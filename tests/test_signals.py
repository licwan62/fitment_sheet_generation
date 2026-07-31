"""Tests for signal detection."""

import pytest

from fitment_agent.agent.signals import SignalDetector, SignalResult


@pytest.fixture
def detector():
    return SignalDetector(
        completion_patterns=[r"本批次完成", r"全部完成", r"可入库全量表"],
        progress_keywords=["更新点", "当前批次进度", "下一步优先处理"],
        similarity_threshold=0.95,
        min_tsv_rows=3,
    )


class TestCompletionSignal:
    def test_detected(self, detector):
        reply = "所有行已处理完毕。本批次完成。"
        result = detector.evaluate(reply, None)
        assert result.is_completion is True

    def test_not_detected(self, detector):
        reply = "正在处理第 3 行，还有一些行需要验证。"
        result = detector.evaluate(reply, None)
        assert result.is_completion is False

    def test_alternative_signal(self, detector):
        reply = "全部完成，所有数据已验证。"
        result = detector.evaluate(reply, None)
        assert result.is_completion is True


class TestFullTable:
    def test_has_full_table(self, detector):
        rows = "\t".join(["col1", "col2", "col3"])
        tsv_block = "```tsv\n" + rows + "\n"
        for i in range(5):
            tsv_block += f"val{i}\tval{i}\tval{i}\n"
        tsv_block += "```"
        reply = f"以下是完整表格：\n{tsv_block}\n更新点: ...\n当前批次进度: ...\n下一步优先处理: ..."
        result = detector.evaluate(reply, None, minimum_rows=3)
        assert result.has_full_table is True
        assert result.full_table_row_count >= 3

    def test_no_full_table(self, detector):
        reply = "本轮更新了两行数据。更新点: ...\n当前批次进度: ...\n下一步优先处理: ..."
        result = detector.evaluate(reply, None)
        assert result.has_full_table is False


class TestRepetition:
    def test_repeated_reply(self, detector):
        reply_a = "这是一段较长的回复内容，包含了很多重要的数据处理信息和更新点。" * 10
        reply_b = reply_a  # identical
        result = detector.evaluate(reply_b, reply_a)
        assert result.is_repeated is True

    def test_different_reply(self, detector):
        reply_a = "第一轮处理了前 10 行数据，主要更新了年份区间。"
        reply_b = "第二轮处理了第 11-20 行，主要补充了尺寸数据。"
        result = detector.evaluate(reply_b, reply_a)
        assert result.is_repeated is False


class TestDeviation:
    def test_deviated(self, detector):
        # No TSV, no progress keywords, no completion, no force_next
        reply = "今天天气不错，适合出去走走。"
        result = detector.evaluate(reply, None)
        assert result.is_deviated is True

    def test_not_deviated_with_progress(self, detector):
        reply = "更新点: 修改了第 5 行\n当前批次进度: 50%\n下一步优先处理: 尺寸验证"
        result = detector.evaluate(reply, None)
        assert result.is_deviated is False


class TestProgressSignals:
    def test_all_present(self, detector):
        reply = "更新点: xxx\n当前批次进度: 60%\n下一步优先处理: yyy"
        result = detector.evaluate(reply, None)
        assert result.has_progress_signals is True

    def test_partial_missing(self, detector):
        reply = "更新点: xxx\n当前批次进度: 60%"
        result = detector.evaluate(reply, None)
        assert result.has_progress_signals is False


class TestForceNext:
    def test_detected(self, detector):
        reply = "请说「下一步」以继续处理。"
        result = detector.evaluate(reply, None)
        assert result.is_force_next is True


class TestSimilarity:
    def test_identical(self):
        assert SignalDetector._similarity("abc", "abc") == 1.0

    def test_empty(self):
        assert SignalDetector._similarity("", "abc") == 0.0
        assert SignalDetector._similarity("abc", "") == 0.0

    def test_both_empty(self):
        assert SignalDetector._similarity("", "") == 0.0

    def test_similar(self):
        a = "hello world"
        b = "hello worl"
        assert SignalDetector._similarity(a, b) > 0.8

    def test_different(self):
        a = "hello"
        b = "xyz123"
        assert SignalDetector._similarity(a, b) < 0.5
