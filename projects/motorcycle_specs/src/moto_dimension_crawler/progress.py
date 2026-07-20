from __future__ import annotations

import csv
import os
import time
from pathlib import Path
from typing import Any, TextIO


MATCH_PROGRESS_COLUMNS = [
    "POSITION", "TOTAL", "COMPLETED_AT", "INPUT_ID", "MAKE", "MODEL",
    "STATUS", "BEST_PAGE_TITLE", "MATCHES", "CANDIDATE_COUNT", "CHECKPOINT",
    "AI_STATUS",
]
FETCH_PROGRESS_COLUMNS = [
    "POSITION", "TOTAL", "COMPLETED_AT", "INPUT_ID", "MAKE", "MODEL",
    "STATUS", "PAGE_TITLE", "SOURCE_URL", "DATA_SOURCE", "FETCHED_AT",
    "CONTENT_HASH",
]
PARSE_PROGRESS_COLUMNS = [
    "POSITION", "TOTAL", "COMPLETED_AT", "INPUT_ID", "MAKE", "MODEL",
    "STATUS", "PARSE_STATUS", "PAGE_TITLE", "SOURCE_URL", "DATA_SOURCE",
    "YEAR", "L-MM", "W-MM", "H-MM", "CONFIDENCE", "ANOMALY_FLAGS", "NOTES",
]


class _DurableCsv:
    """Flush every CSV row, but amortize expensive physical-disk sync calls."""

    def __init__(self, path: Path, columns: list[str], sync_every: int = 50, sync_interval: float = 1.0):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.handle: TextIO = path.open("w", encoding="utf-8-sig", newline="")
        self.writer = csv.DictWriter(self.handle, fieldnames=columns, extrasaction="ignore")
        self.sync_every = max(1, sync_every)
        self.sync_interval = max(0.1, sync_interval)
        self.pending_rows = 0
        self.last_sync = time.monotonic()
        self.writer.writeheader()
        self._sync()

    def write(self, row: dict[str, Any]) -> None:
        self.writer.writerow({key: "" if value is None else value for key, value in row.items()})
        self.handle.flush()
        self.pending_rows += 1
        if self.pending_rows >= self.sync_every or time.monotonic() - self.last_sync >= self.sync_interval:
            self._sync()

    def _sync(self) -> None:
        self.handle.flush()
        os.fsync(self.handle.fileno())
        self.pending_rows = 0
        self.last_sync = time.monotonic()

    def close(self) -> None:
        if self.pending_rows:
            self._sync()
        self.handle.close()


class ProgressFiles:
    """Human-readable, crash-durable progress outputs for the three pipeline stages."""

    def __init__(self, output: Path):
        self.match = _DurableCsv(output / "match_progress.csv", MATCH_PROGRESS_COLUMNS)
        self.fetch = _DurableCsv(output / "fetch_progress.csv", FETCH_PROGRESS_COLUMNS)
        self.parse = _DurableCsv(output / "parse_progress.csv", PARSE_PROGRESS_COLUMNS)

    def close(self) -> None:
        self.match.close()
        self.fetch.close()
        self.parse.close()
