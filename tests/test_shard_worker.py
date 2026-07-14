"""Tests for the shard worker state machine with a mock LLM backend."""

import asyncio
from pathlib import Path
from typing import List

import pytest

from fitment_agent.agent.shard_worker import ShardWorker, ShardResult
from fitment_agent.agent.signals import SignalDetector
from fitment_agent.agent.messages import MessageBuilder
from fitment_agent.agent.state import ShardState
from fitment_agent.llm.protocol import LLMBackend, LLMResponse, ConversationState
from fitment_agent.templates.us_edmunds import UsEdmundsTemplate


# ---------------------------------------------------------------------------
# Mock LLM Backend
# ---------------------------------------------------------------------------

class MockLLMBackend(LLMBackend):
    """A mock LLM backend that returns pre-scripted replies."""

    def __init__(self, replies: List[str]):
        self._replies = list(replies)
        self._index = 0
        self._round = 0
        self._sent_messages: List[str] = []

    async def start_conversation(self) -> None:
        self._index = 0
        self._round = 0

    async def send_message(self, message: str) -> None:
        self._sent_messages.append(message)

    async def wait_for_reply(self, *, timeout: int = 900) -> LLMResponse:
        self._round += 1
        if self._index < len(self._replies):
            text = self._replies[self._index]
            self._index += 1
        else:
            text = "no more replies"
        return LLMResponse(
            text=text,
            round_number=self._round,
            is_complete=True,
        )

    async def get_state(self) -> ConversationState:
        return ConversationState(is_generating=False, is_ready=True)

    async def close(self) -> None:
        pass


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def template():
    return UsEdmundsTemplate()


@pytest.fixture
def signals(template):
    return SignalDetector(
        completion_patterns=template.get_completion_signals(),
        progress_keywords=template.get_progress_keywords(),
    )


@pytest.fixture
def messages(template):
    return MessageBuilder(template)


@pytest.fixture
def output_dir(tmp_path):
    d = tmp_path / "output"
    d.mkdir()
    return d


SAMPLE_TSV = "主车型\t分类\t品牌\nChevrolet Silverado\t皮卡\tChevrolet"


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestShardState:
    def test_terminal_states(self):
        assert ShardState.COMPLETE.is_terminal
        assert ShardState.REPEATED.is_terminal
        assert ShardState.DEVIATED.is_terminal
        assert ShardState.MAX_ROUNDS.is_terminal
        assert ShardState.ERROR.is_terminal
        assert not ShardState.INIT.is_terminal
        assert not ShardState.WAITING_REPLY.is_terminal

    def test_sending_states(self):
        assert ShardState.SENDING_INITIAL.is_sending
        assert ShardState.SENDING_CONTINUE.is_sending
        assert not ShardState.WAITING_REPLY.is_sending

    def test_status_string(self):
        assert ShardState.COMPLETE.to_status_string() == "成功"
        assert ShardState.REPEATED.to_status_string() == "重复终止"


class TestShardWorker:
    @pytest.mark.asyncio
    async def test_complete_on_first_round(self, template, signals, messages, output_dir):
        """LLM returns completion + full table on first round."""
        tsv_rows = "主车型\t分类\n"
        for i in range(5):
            tsv_rows += f"Car{i}\tSUV\n"
        reply = (
            f"以下是完整表格：\n```\n{tsv_rows}```\n"
            f"更新点: 全部完成\n"
            f"当前批次进度: 100%\n"
            f"下一步优先处理: 无\n"
            f"本批次完成"
        )
        backend = MockLLMBackend([reply])
        worker = ShardWorker(
            shard_name="test_part_01",
            tsv_content=SAMPLE_TSV,
            requirement_text="test requirement",
            backend=backend,
            template=template,
            signals=signals,
            messages=messages,
            max_rounds=10,
            output_dir=output_dir,
        )
        result = await worker.process()
        assert result.status == "成功"
        assert result.rounds_completed == 1
        assert result.output_file is not None
        assert result.output_file.exists()

    @pytest.mark.asyncio
    async def test_continue_then_complete(self, template, signals, messages, output_dir):
        """LLM needs 2 rounds: progress first, then completion."""
        tsv_rows = "主车型\t分类\n"
        for i in range(5):
            tsv_rows += f"Car{i}\tSUV\n"

        reply1 = (
            f"第一轮处理\n```\n{tsv_rows}```\n"
            f"更新点: 验证了年份\n"
            f"当前批次进度: 50%\n"
            f"下一步优先处理: 尺寸"
        )
        reply2 = (
            f"最终表格\n```\n{tsv_rows}```\n"
            f"更新点: 补充了尺寸\n"
            f"当前批次进度: 100%\n"
            f"下一步优先处理: 无\n"
            f"本批次完成"
        )
        backend = MockLLMBackend([reply1, reply2])
        worker = ShardWorker(
            shard_name="test_part_02",
            tsv_content=SAMPLE_TSV,
            requirement_text="test requirement",
            backend=backend,
            template=template,
            signals=signals,
            messages=messages,
            max_rounds=10,
            output_dir=output_dir,
        )
        result = await worker.process()
        assert result.status == "成功"
        assert result.rounds_completed == 2
        assert result.messages_sent >= 2  # initial + continue

    @pytest.mark.asyncio
    async def test_max_rounds(self, template, signals, messages, output_dir):
        """Worker should stop at max_rounds."""
        # Each reply has progress but never completion, and each is unique
        # to avoid repetition detection
        replies = []
        for i in range(20):
            replies.append(
                f"```\n主车型\t分类\nCar{i}\tSUV\n```\n"
                f"更新点: round {i}\n当前批次进度: {i}%\n下一步优先处理: item {i}"
            )
        backend = MockLLMBackend(replies)
        worker = ShardWorker(
            shard_name="test_max",
            tsv_content=SAMPLE_TSV,
            requirement_text="test",
            backend=backend,
            template=template,
            signals=signals,
            messages=messages,
            max_rounds=3,
            output_dir=output_dir,
        )
        result = await worker.process()
        assert result.status == "次数上限终止"
        assert result.rounds_completed >= 3

    @pytest.mark.asyncio
    async def test_repeated_reply(self, template, signals, messages, output_dir):
        """Worker should detect repeated replies and stop."""
        reply = (
            "```\n主车型\t分类\nCar1\tSUV\n```\n"
            "更新点: x\n当前批次进度: 50%\n下一步优先处理: y"
        )
        # Same reply twice → repetition
        backend = MockLLMBackend([reply, reply])
        worker = ShardWorker(
            shard_name="test_repeat",
            tsv_content=SAMPLE_TSV,
            requirement_text="test",
            backend=backend,
            template=template,
            signals=signals,
            messages=messages,
            max_rounds=10,
            output_dir=output_dir,
        )
        result = await worker.process()
        assert result.status == "重复终止"

    @pytest.mark.asyncio
    async def test_output_file_created(self, template, signals, messages, output_dir):
        """Verify that the output markdown file is written."""
        tsv_rows = "主车型\t分类\n"
        for i in range(5):
            tsv_rows += f"Car{i}\tSUV\n"
        reply = (
            f"```\n{tsv_rows}```\n"
            f"更新点: done\n当前批次进度: 100%\n下一步优先处理: none\n本批次完成"
        )
        backend = MockLLMBackend([reply])
        worker = ShardWorker(
            shard_name="test_output",
            tsv_content=SAMPLE_TSV,
            requirement_text="test",
            backend=backend,
            template=template,
            signals=signals,
            messages=messages,
            max_rounds=10,
            output_dir=output_dir,
        )
        result = await worker.process()
        assert result.output_file is not None
        content = result.output_file.read_text(encoding="utf-8")
        assert "Round 1" in content
