"""Pipeline orchestrator — coordinates the full enrichment workflow."""

from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from ..config.models import InputListConfig, RequirementConfig
from ..llm.protocol import LLMBackend
from ..templates.base import RequirementTemplate
from ..templates.registry import get_template
from ..vehicle.expander import VehicleExpander
from ..vehicle.tsv_splitter import split_tsv
from .messages import MessageBuilder
from .shard_worker import ShardResult, ShardWorker
from .signals import SignalDetector

console = Console()


@dataclass
class PipelineResult:
    """Summary of a full pipeline run."""

    total_shards: int = 0
    successful: int = 0
    repeated: int = 0
    max_rounds: int = 0
    deviated: int = 0
    errors: int = 0
    shard_results: list[ShardResult] = field(default_factory=list)
    merged_output_path: Path | None = None
    summary_path: Path | None = None


class PipelineOrchestrator:
    """Coordinates: expand → build TSV → split → enrich shards → merge.

    This replaces run_from_config.ps1 + qclaw_fitment_automation.ps1
    with a single Python entry point.
    """

    def __init__(
        self,
        *,
        requirement_cfg: RequirementConfig,
        input_list: InputListConfig,
        project_dir: Path,
        backend_factory: callable,
        max_rounds: int | None = None,
        chunk_size: int = 50,
    ) -> None:
        self._req_cfg = requirement_cfg
        self._input_list = input_list
        self._project_dir = project_dir
        self._backend_factory = backend_factory
        self._max_rounds = max_rounds or requirement_cfg.params.max_rounds or 150
        self._chunk_size = (
            requirement_cfg.params.chunk_size or chunk_size
        )

        self._template: RequirementTemplate = get_template(requirement_cfg.template)
        self._requirement_text = self._template.get_requirement_text(
            requirement_cfg.params.model_dump()
        )

    async def run(self) -> PipelineResult:
        """Execute the full pipeline."""
        result = PipelineResult()
        self._project_dir.mkdir(parents=True, exist_ok=True)

        # Step 1: Expand vehicles into seed TSV
        console.print("[bold cyan]Step 1: Expanding vehicles...[/bold cyan]")
        tsv_content = await self._expand_vehicles()

        # Step 2: Split into shards
        console.print("[bold cyan]Step 2: Splitting into shards...[/bold cyan]")
        input_dir = self._project_dir / "input"
        shards = split_tsv(tsv_content, self._chunk_size, input_dir)
        result.total_shards = len(shards)
        console.print(f"  Split into {len(shards)} shards (chunk_size={self._chunk_size})")

        # Step 3: Process each shard
        console.print("[bold cyan]Step 3: Processing shards...[/bold cyan]")
        output_dir = self._project_dir / "output"
        checkpoint_path = self._project_dir / "checkpoint.json"
        completed = self._load_checkpoint(checkpoint_path)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Processing shards", total=len(shards))

            for shard_name, shard_content in shards:
                if shard_name in completed:
                    progress.update(task, advance=1, description=f"Skipped {shard_name}")
                    continue

                progress.update(task, description=f"Processing {shard_name}")
                backend: LLMBackend = self._backend_factory()
                signals = SignalDetector(
                    completion_patterns=self._template.get_completion_signals(),
                    progress_keywords=self._template.get_progress_keywords(),
                )
                messages = MessageBuilder(self._template)

                worker = ShardWorker(
                    shard_name=shard_name,
                    tsv_content=shard_content,
                    requirement_text=self._requirement_text,
                    backend=backend,
                    template=self._template,
                    signals=signals,
                    messages=messages,
                    max_rounds=self._max_rounds,
                    output_dir=output_dir,
                )
                shard_result = await worker.process()
                result.shard_results.append(shard_result)

                # Tally
                status = shard_result.status
                if status == "成功":
                    result.successful += 1
                elif status == "重复终止":
                    result.repeated += 1
                elif status == "次数上限终止":
                    result.max_rounds += 1
                elif status == "偏离终止":
                    result.deviated += 1
                else:
                    result.errors += 1

                # Checkpoint
                completed.add(shard_name)
                self._save_checkpoint(checkpoint_path, completed)
                progress.update(task, advance=1)

                await backend.close()

        # Step 4: Summary
        console.print("[bold cyan]Step 4: Generating summary...[/bold cyan]")
        result.summary_path = self._write_summary(result)
        self._print_summary(result)

        return result

    async def _expand_vehicles(self) -> str:
        """Expand vehicle entries into a seed TSV."""
        # If user provided a prebuilt TSV, use it directly
        if self._input_list.prebuilt_tsv:
            return Path(self._input_list.prebuilt_tsv).read_text(encoding="utf-8")

        expander = VehicleExpander(
            backend_factory=self._backend_factory,
            template=self._template,
        )
        return await expander.expand_to_tsv(self._input_list.vehicles)

    def _load_checkpoint(self, path: Path) -> set[str]:
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            return set(data.get("completed", []))
        return set()

    def _save_checkpoint(self, path: Path, completed: set[str]) -> None:
        path.write_text(
            json.dumps({"completed": list(completed)}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _write_summary(self, result: PipelineResult) -> Path:
        summary_path = self._project_dir / "summary.txt"
        lines = [
            f"Pipeline Summary - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            f"=" * 50,
            f"Total shards: {result.total_shards}",
            f"Successful:   {result.successful}",
            f"Repeated:     {result.repeated}",
            f"Max rounds:   {result.max_rounds}",
            f"Deviated:     {result.deviated}",
            f"Errors:       {result.errors}",
            "",
            "Per-shard details:",
        ]
        for sr in result.shard_results:
            lines.append(
                f"  {sr.shard_name}: {sr.status} "
                f"(rounds={sr.rounds_completed}, msgs={sr.messages_sent})"
            )
        summary_path.write_text("\n".join(lines), encoding="utf-8")
        return summary_path

    def _print_summary(self, result: PipelineResult) -> None:
        console.print()
        console.print("[bold]Pipeline Complete[/bold]")
        console.print(f"  Total: {result.total_shards} | "
                      f"[green]OK: {result.successful}[/green] | "
                      f"[yellow]Repeated: {result.repeated}[/yellow] | "
                      f"[red]Errors: {result.errors}[/red]")
