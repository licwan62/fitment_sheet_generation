"""Abstract base for requirement templates (US Edmunds, EU AutoData, etc.)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class DataContract:
    """Defines the expected output schema for a template."""

    columns: list[str]
    auto_empty_columns: list[str] = field(default_factory=list)
    subseries_columns: list[str] = field(default_factory=list)
    subseries_auto_empty: list[str] = field(default_factory=list)
    instructions: list[str] = field(default_factory=list)


class RequirementTemplate(ABC):
    """Every market/mode gets a concrete subclass that knows how to:
    - Render the full requirement text with user params
    - Define the output data contract (columns, auto-empty, etc.)
    - Build the initial prompt and follow-up messages
    """

    name: str

    @abstractmethod
    def get_requirement_text(self, params: dict) -> str:
        """Return the full requirement markdown, with params substituted."""

    @abstractmethod
    def get_data_contract(self) -> DataContract:
        """Return the expected output schema."""

    @abstractmethod
    def build_initial_prompt(
        self, requirement_text: str, tsv_content: str, filename: str
    ) -> str:
        """Build the first message sent to the LLM for a shard."""

    @abstractmethod
    def get_continue_message(self) -> str:
        """Message to send when the LLM should proceed to the next round."""

    @abstractmethod
    def get_missing_signals_message(self) -> str:
        """Message when the reply lacks required progress indicators."""

    @abstractmethod
    def get_full_table_request_message(self) -> str:
        """Message to request the complete output table."""

    @abstractmethod
    def get_completion_fix_message(self) -> str:
        """Message when completion signal is detected but full table is missing."""

    @abstractmethod
    def get_completion_signals(self) -> list[str]:
        """Regex patterns that indicate the LLM has finished processing."""

    @abstractmethod
    def get_progress_keywords(self) -> list[str]:
        """Keywords that must appear in a healthy round reply."""
