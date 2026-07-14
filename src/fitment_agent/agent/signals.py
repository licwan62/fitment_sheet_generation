"""Signal detection — evaluates LLM replies to decide the next action.

This is a direct port of the PowerShell Test-* functions into Python.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class SignalResult:
    """Result of evaluating one LLM reply."""

    is_completion: bool = False
    is_full_table_request: bool = False
    is_force_next: bool = False
    has_progress_signals: bool = False
    is_repeated: bool = False
    is_deviated: bool = False
    has_full_table: bool = False
    full_table_row_count: int = 0


class SignalDetector:
    """Evaluates LLM replies against completion, repetition, and deviation rules."""

    def __init__(
        self,
        completion_patterns: list[str],
        progress_keywords: list[str],
        *,
        similarity_threshold: float = 0.95,
        min_tsv_rows: int = 5,
    ) -> None:
        self._completion_re = [re.compile(p) for p in completion_patterns]
        self._progress_keywords = progress_keywords
        self._similarity_threshold = similarity_threshold
        self._min_tsv_rows = min_tsv_rows

    def evaluate(
        self,
        reply: str,
        previous_reply: str | None,
        *,
        minimum_rows: int | None = None,
    ) -> SignalResult:
        """Evaluate all signals for a single reply."""
        result = SignalResult()

        # Completion signal
        result.is_completion = any(p.search(reply) for p in self._completion_re)

        # Full table presence
        tsv_rows = self._count_tsv_rows(reply)
        result.has_full_table = tsv_rows >= (minimum_rows or self._min_tsv_rows)
        result.full_table_row_count = tsv_rows

        # Full table request signal
        result.is_full_table_request = bool(
            re.search(r"可入库全量表|请.*输出.*完整.*表", reply)
        )

        # Force-next signal (LLM asks user to say 下一步)
        result.is_force_next = bool(re.search(r"请.*[说发送].*下一步", reply))

        # Progress signals
        if self._progress_keywords:
            result.has_progress_signals = all(
                kw in reply for kw in self._progress_keywords
            )

        # Repetition detection (Levenshtein similarity)
        if previous_reply:
            sim = self._similarity(reply, previous_reply)
            result.is_repeated = sim >= self._similarity_threshold

        # Deviation detection (no TSV, no progress keywords, no completion)
        if (
            not result.has_full_table
            and not result.has_progress_signals
            and not result.is_completion
            and not result.is_force_next
        ):
            result.is_deviated = True

        return result

    @staticmethod
    def _count_tsv_rows(text: str) -> int:
        """Count data rows (excluding headers) inside TSV code blocks."""
        count = 0
        in_block = False
        header_skipped = False
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("```"):
                in_block = not in_block
                header_skipped = False
                continue
            if in_block and stripped and "\t" in stripped:
                if not header_skipped:
                    header_skipped = True  # skip the header row
                    continue
                count += 1
        return count

    @staticmethod
    def _similarity(a: str, b: str) -> float:
        """Compute character-level similarity ratio (Levenshtein-based)."""
        if not a or not b:
            return 0.0
        if a == b:
            return 1.0
        # Use a fast approximation: ratio of common characters
        la, lb = len(a), len(b)
        if la > 10000 or lb > 10000:
            # For very long texts, sample the first 5000 chars
            a = a[:5000]
            b = b[:5000]
            la, lb = len(a), len(b)
        # Simple Levenshtein via matrix (bounded for performance)
        if abs(la - lb) / max(la, lb) > 0.3:
            return 0.0  # Fast reject for very different lengths
        # Use a rolling two-row DP approach
        prev = list(range(lb + 1))
        curr = [0] * (lb + 1)
        for i, ca in enumerate(a, 1):
            curr[0] = i
            for j, cb in enumerate(b, 1):
                cost = 0 if ca == cb else 1
                curr[j] = min(prev[j] + 1, curr[j - 1] + 1, prev[j - 1] + cost)
            prev, curr = curr, prev
        distance = prev[lb]
        return 1.0 - distance / max(la, lb)
