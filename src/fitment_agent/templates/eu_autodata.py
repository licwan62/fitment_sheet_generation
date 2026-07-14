"""EU AutoData requirement template adapter."""

from __future__ import annotations

from pathlib import Path

from .base import DataContract, RequirementTemplate

_PROMPTS_DIR = Path(__file__).parent / "prompts"


class EuAutodataTemplate(RequirementTemplate):
    name = "eu_autodata"

    def get_requirement_text(self, params: dict) -> str:
        md_path = _PROMPTS_DIR / "eu_autodata.md"
        text = md_path.read_text(encoding="utf-8")
        sources = params.get("data_sources", [
            "Auto-Data", "Car.info", "UltimateSpecs", "Automobile-Catalog", "Parkers"
        ])
        text = text.replace("{{DATA_SOURCES}}", " > ".join(sources))
        return text

    def get_data_contract(self) -> DataContract:
        return DataContract(
            columns=[
                "Ktype", "Make", "Model", "BodyStyle", "Generation",
                "YearFrom", "YearTo", "EngineCode", "Power_kW", "Fuel",
                "Transmission", "DIMENSION_GROUP_ID",
                "Length_mm", "Width_mm", "Height_mm", "Wheelbase_mm",
                "CacheStatus", "EndDateStatus", "备注", "迭代状态",
            ],
            auto_empty_columns=["CacheStatus", "EndDateStatus"],
            subseries_columns=[],
            subseries_auto_empty=[],
            instructions=[
                "每个 Ktype 独立解析尺寸，不可因发动机相似而跳过",
                "尺寸存储在 DIMENSION_GROUP 级别，非 Ktype 级别",
            ],
        )

    def build_initial_prompt(
        self, requirement_text: str, tsv_content: str, filename: str
    ) -> str:
        return (
            f"请严格按照以下 requirement 处理 TSV 数据。\n\n"
            f"--- REQUIREMENT START ---\n{requirement_text}\n--- REQUIREMENT END ---\n\n"
            f"以下是待处理的 TSV 文件 `{filename}`：\n\n```\n{tsv_content}\n```\n\n"
            f"请开始第一步处理。"
        )

    def get_continue_message(self) -> str:
        return (
            "下一步\n\n"
            "请按以下格式继续：\n"
            "1. **更新点**：本轮处理了哪些 Ktype\n"
            "2. **完整 TSV 代码块**：所有行最新状态\n"
            "3. **当前批次进度**：已完成/待处理\n"
            "4. **下一步优先处理**"
        )

    def get_missing_signals_message(self) -> str:
        return (
            "你的回复缺少必要的进度信号。请确保包含：\n"
            "- 完整 TSV 代码块\n"
            "- 更新点\n"
            "- 当前批次进度\n"
            "- 下一步优先处理方向"
        )

    def get_full_table_request_message(self) -> str:
        return "请输出完整的 TSV 表格（所有 Ktype 行），不要省略。"

    def get_completion_fix_message(self) -> str:
        return (
            "你标记了完成，但回复中缺少完整 TSV 表格。"
            "请输出包含所有 Ktype 行的完整 TSV。"
        )

    def get_completion_signals(self) -> list[str]:
        return [r"本批次完成", r"全部完成", r"可入库"]

    def get_progress_keywords(self) -> list[str]:
        return ["更新点", "当前批次进度", "下一步优先处理"]
