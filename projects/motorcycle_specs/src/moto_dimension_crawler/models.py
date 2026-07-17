from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class InputRecord:
    input_id: str
    make: str
    model: str
    vehicle_type: str = ""
    make_normalized: str = ""
    model_normalized: str = ""
    model_compact: str = ""
    number_tokens: list[str] = field(default_factory=list)
    word_tokens: list[str] = field(default_factory=list)

    def dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class Candidate:
    input_id: str
    title: str
    url: str
    source_make: str = ""
    source_model: str = ""
    source_version: str = ""
    source_year: str = ""
    score: int = 0
    status: str = "REVIEW"
    reason: str = ""
    discovery_method: str = "INDEX"


@dataclass(slots=True)
class DimensionResult:
    values: dict[str, float | None] = field(default_factory=dict)
    raw: dict[str, str] = field(default_factory=dict)
    width_scope: str = "UNKNOWN"
    height_scope: str = "UNKNOWN"
    accessory_status: str = "UNKNOWN"
    parse_status: str = "NO_DIMENSION"
    anomaly_flags: list[str] = field(default_factory=list)
    dimension_raw: str = ""

