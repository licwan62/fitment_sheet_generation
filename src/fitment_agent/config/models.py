"""Pydantic models for user-facing YAML configuration files."""

from typing import List, Literal, Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# requirement.yaml
# ---------------------------------------------------------------------------

class TemplateParams(BaseModel):
    """User-customizable parameters merged into the requirement template."""

    market: str = "US"
    data_sources: List[str] = Field(default_factory=lambda: ["Edmunds", "KBB", "NHTSA"])
    focus_fields: List[str] = Field(default_factory=lambda: ["dimensions", "year_range", "generation"])
    extra_instructions: List[str] = Field(default_factory=list)
    # Overrides (optional)
    max_rounds: Optional[int] = None
    chunk_size: Optional[int] = None
    model: Optional[str] = None


class RequirementConfig(BaseModel):
    """Schema for requirement.yaml — the file non-technical users edit to
    control *how* the LLM processes vehicle data."""

    template: Literal["us_edmunds", "eu_autodata"]
    params: TemplateParams = Field(default_factory=TemplateParams)


# ---------------------------------------------------------------------------
# input_list.yaml
# ---------------------------------------------------------------------------

class VehicleEntry(BaseModel):
    """One vehicle to process. Only make + model are required; the agent
    expands the rest (generations, years, body styles) automatically."""

    make: str
    model: str
    year_from: Optional[int] = None
    year_to: Optional[int] = None
    body_styles: Optional[List[str]] = None
    generations: Optional[List[str]] = None
    notes: Optional[str] = None


class InputListConfig(BaseModel):
    """Schema for input_list.yaml — the file non-technical users edit to
    specify *which* vehicles to process."""

    vehicles: List[VehicleEntry]
    prebuilt_tsv: Optional[str] = None
