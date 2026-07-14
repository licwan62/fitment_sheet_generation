"""YAML loading and validation for user-facing config files."""

from __future__ import annotations

from pathlib import Path

import yaml

from .models import InputListConfig, RequirementConfig


def load_requirement(path: Path) -> RequirementConfig:
    """Load and validate requirement.yaml."""
    raw = yaml.safe_load(path.read_text(encoding="utf-8-sig"))
    return RequirementConfig.model_validate(raw)


def load_input_list(path: Path) -> InputListConfig:
    """Load and validate input_list.yaml."""
    raw = yaml.safe_load(path.read_text(encoding="utf-8-sig"))
    return InputListConfig.model_validate(raw)
