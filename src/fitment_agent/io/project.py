"""Project directory layout management."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class ProjectLayout:
    """Manages the standard project directory structure."""

    root: Path

    @property
    def input_dir(self) -> Path:
        return self.root / "input"

    @property
    def output_dir(self) -> Path:
        return self.root / "output"

    @property
    def log_path(self) -> Path:
        return self.root / "log.csv"

    @property
    def summary_path(self) -> Path:
        return self.root / "summary.txt"

    @property
    def checkpoint_path(self) -> Path:
        return self.root / "checkpoint.json"

    def ensure_dirs(self) -> None:
        self.input_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def get_result_files(self) -> list[Path]:
        """Return all shard result markdown files."""
        if not self.output_dir.exists():
            return []
        return sorted(self.output_dir.glob("*_result.md"))
