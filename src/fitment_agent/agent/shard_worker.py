"""Per-shard multi-round agent loop — the heart of the enrichment process."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from rich.console import Console

from ..llm.protocol import LLMBackend, LLMResponse
from ..templates.base import RequirementTemplate
from .messages import MessageBuilder
from .signals import SignalDetector, SignalResult
from .state import ShardState

console = Console()


@dataclass
class ShardResult:
    """Outcome of processing one shard."""

    shard_name: str
    status: str = "进行中"
    rounds_completed: int = 0
    messages_sent: int = 0
    output_file: Path | None = None
    remarks: str = ""
    start_time: datetime = field(default_factory=datetime.now)
    end_time: datetime | None = None


class ShardWorker:
    """Drives one TSV shard through a multi-round LLM conversation.

    This implements the same state machine that was previously in
    qclaw_fitment_automation.ps1 Process-TSVFile (lines 1681-1844),
    but in clean Python with async I/O.
    """

    def __init__(
        self,
        *,
        shard_name: str,
        tsv_content: str,
        requirement_text: str,
        backend: LLMBackend,
        template: RequirementTemplate,
        signals: SignalDetector,
        messages: MessageBuilder,
        max_rounds: int = 150,
        output_dir: Path,
    ) -> None:
        self._shard_name = shard_name
        self._tsv_content = tsv_content
        self._requirement_text = requirement_text
        self._backend = backend
        self._template = template
        self._signals = signals
        self._messages = messages
        self._max_rounds = max_rounds
        self._output_dir = output_dir

        self._state = ShardState.INIT
        self._result = ShardResult(shard_name=shard_name)
        self._round = 0
        self._previous_reply: str | None = None
        self._reply_history: list[str] = []

    async def process(self) -> ShardResult:
        """Run the shard through the full agent loop until terminal state."""
        await self._backend.start_conversation()

        while not self._state.is_terminal:
            try:
                await self._step()
            except Exception as exc:
                self._state = ShardState.ERROR
                self._result.remarks = str(exc)
                console.print(f"[red]  Shard {self._shard_name} error: {exc}[/red]")

        self._result.end_time = datetime.now()
        self._result.status = self._state.to_status_string()
        self._save_output()
        return self._result

    async def _step(self) -> None:
        """Execute one state transition."""
        s = self._state
        if s == ShardState.INIT:
            self._state = ShardState.SENDING_INITIAL

        elif s == ShardState.SENDING_INITIAL:
            msg = self._messages.build_initial_prompt(
                self._requirement_text, self._tsv_content, self._shard_name
            )
            await self._backend.send_message(msg)
            self._result.messages_sent += 1
            self._state = ShardState.WAITING_REPLY

        elif s == ShardState.WAITING_REPLY:
            reply = await self._backend.wait_for_reply()
            self._round = reply.round_number
            self._result.rounds_completed = self._round
            self._reply_history.append(reply.text)
            self._state = ShardState.EVALUATING_REPLY

        elif s == ShardState.EVALUATING_REPLY:
            self._evaluate_and_transition()

        elif s == ShardState.SENDING_CONTINUE:
            await self._backend.send_message(
                self._messages.build_continue_message()
            )
            self._result.messages_sent += 1
            self._state = ShardState.WAITING_REPLY

        elif s == ShardState.SENDING_FULL_TABLE_REQUEST:
            await self._backend.send_message(
                self._messages.build_full_table_request_message()
            )
            self._result.messages_sent += 1
            self._state = ShardState.WAITING_REPLY

        elif s == ShardState.SENDING_FIX_REQUEST:
            await self._backend.send_message(
                self._messages.build_completion_fix_message()
            )
            self._result.messages_sent += 1
            self._state = ShardState.WAITING_REPLY

        elif s == ShardState.SENDING_MISSING_SIGNALS:
            await self._backend.send_message(
                self._messages.build_missing_signals_message()
            )
            self._result.messages_sent += 1
            self._state = ShardState.WAITING_REPLY

    def _evaluate_and_transition(self) -> None:
        """Decide the next state based on signal evaluation of the latest reply."""
        current_reply = self._reply_history[-1] if self._reply_history else ""
        min_rows = len(self._tsv_content.strip().splitlines()) - 1  # minus header

        sig: SignalResult = self._signals.evaluate(
            current_reply,
            self._previous_reply,
            minimum_rows=max(min_rows, 5),
        )

        console.print(
            f"  [dim]Round {self._round}: "
            f"completion={sig.is_completion}, "
            f"full_table={sig.has_full_table} ({sig.full_table_row_count} rows), "
            f"progress={sig.has_progress_signals}, "
            f"repeated={sig.is_repeated}, "
            f"deviated={sig.is_deviated}[/dim]"
        )

        self._previous_reply = current_reply

        # Check max rounds first
        if self._round >= self._max_rounds:
            self._state = ShardState.MAX_ROUNDS
            return

        # Terminal conditions
        if sig.is_repeated:
            self._state = ShardState.REPEATED
            return

        if sig.is_deviated:
            self._state = ShardState.DEVIATED
            return

        # Completion
        if sig.is_completion and sig.has_full_table:
            self._state = ShardState.COMPLETE
            return

        if sig.is_completion and not sig.has_full_table:
            self._state = ShardState.SENDING_FIX_REQUEST
            return

        # Full table request signal
        if sig.is_full_table_request and not sig.has_full_table:
            self._state = ShardState.SENDING_FULL_TABLE_REQUEST
            return

        # Missing progress signals
        if not sig.has_progress_signals and not sig.is_force_next:
            self._state = ShardState.SENDING_MISSING_SIGNALS
            return

        # Normal continue
        self._state = ShardState.SENDING_CONTINUE

    def _save_output(self) -> None:
        """Save the reply history to the output directory."""
        self._output_dir.mkdir(parents=True, exist_ok=True)
        output_path = self._output_dir / f"{self._shard_name}_result.md"
        with output_path.open("w", encoding="utf-8") as f:
            for i, reply in enumerate(self._reply_history, 1):
                f.write(f"--- Round {i} ---\n\n{reply}\n\n")
        self._result.output_file = output_path
