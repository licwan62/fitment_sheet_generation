"""Context-aware message builder for the agent loop."""

from __future__ import annotations

from ..templates.base import RequirementTemplate


class MessageBuilder:
    """Builds the appropriate message for each state transition.

    Delegates to the template for content, but adds context like
    the data contract columns and current round number.
    """

    def __init__(self, template: RequirementTemplate) -> None:
        self._template = template

    def build_initial_prompt(
        self, requirement_text: str, tsv_content: str, filename: str
    ) -> str:
        contract = self._template.get_data_contract()
        columns_header = "\t".join(contract.columns)
        instructions = "\n".join(f"- {inst}" for inst in contract.instructions)
        return (
            f"{self._template.build_initial_prompt(requirement_text, tsv_content, filename)}\n\n"
            f"输出 TSV 表头必须严格为：\n```\n{columns_header}\n```\n\n"
            f"全局约束：\n{instructions}\n"
        )

    def build_continue_message(self) -> str:
        return self._template.get_continue_message()

    def build_missing_signals_message(self) -> str:
        return self._template.get_missing_signals_message()

    def build_full_table_request_message(self) -> str:
        return self._template.get_full_table_request_message()

    def build_completion_fix_message(self) -> str:
        return self._template.get_completion_fix_message()
