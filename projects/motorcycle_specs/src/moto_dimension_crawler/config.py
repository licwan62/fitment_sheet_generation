from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_config(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def load_aliases(config_dir: Path) -> tuple[dict, dict]:
    def read(name: str, key: str) -> dict:
        path = config_dir / name
        if not path.exists():
            return {}
        with path.open("r", encoding="utf-8") as fh:
            return (yaml.safe_load(fh) or {}).get(key, {})

    return read("brand_aliases.yaml", "brand_aliases"), read("model_aliases.yaml", "model_aliases")


def load_manual_pages(config_dir: Path) -> list[dict[str, Any]]:
    path = config_dir / "manual_pages.yaml"
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as fh:
        return (yaml.safe_load(fh) or {}).get("manual_pages", [])
