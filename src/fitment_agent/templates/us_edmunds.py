"""US Edmunds requirement template adapter."""

from __future__ import annotations

from pathlib import Path

from .base import DataContract, RequirementTemplate

_PROMPTS_DIR = Path(__file__).parent / "prompts"


class UsEdmundsTemplate(RequirementTemplate):
    name = "us_edmunds"

    def get_requirement_text(self, params: dict) -> str:
        md_path = _PROMPTS_DIR / "us_edmunds.md"
        text = md_path.read_text(encoding="utf-8")
        # Substitute data_sources list into the requirement
        sources = params.get("data_sources", ["Edmunds", "KBB", "NHTSA"])
        text = text.replace(
            "{{DATA_SOURCES}}",
            " > ".join(sources),
        )
        return text

    def get_data_contract(self) -> DataContract:
        return DataContract(
            columns=[
                "主车型", "年份区间", "结构", "对应尺码", "品牌", "前台车型",
                "排序依据车型", "子车系", "分类", "版本", "门数", "代际",
                "区间最小年份", "区间最大年份",
                "max_length_in", "max_width_in", "max_height_in",
                "max_length_cm", "max_width_cm", "max_height_cm",
                "驾驶室类型", "货斗长度_ft", "长度余量", "无尺码原因",
                "参考车型", "备注", "迭代状态",
            ],
            auto_empty_columns=[
                "对应尺码", "排序依据车型", "子车系",
                "区间最小年份", "区间最大年份",
                "max_length_cm", "max_width_cm", "max_height_cm",
                "长度余量", "无尺码原因",
            ],
            subseries_columns=["Year", "主车型", "结构", "版本", "候选车型", "匹配数量"],
            subseries_auto_empty=["匹配数量"],
            instructions=[
                "不得新增当前 TSV 年份范围外的年代、代际或车型行",
                "输出顺序必须保持输入 split 第一条到最后一条的边界",
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
            "1. **更新点**：本轮修改了哪些行\n"
            "2. **完整 TSV 代码块**：包含所有行的最新状态\n"
            "3. **当前批次进度**：已完成/待处理\n"
            "4. **下一步优先处理**：下一轮的重点"
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
        return "请输出完整的 TSV 表格（所有行），不要省略。"

    def get_completion_fix_message(self) -> str:
        return (
            "你标记了完成，但回复中缺少完整 TSV 表格。"
            "请输出包含所有行的完整 TSV，然后再标记本批次完成。"
        )

    def get_completion_signals(self) -> list[str]:
        return [
            r"本批次完成",
            r"全部完成",
            r"可入库全量表",
        ]

    def get_progress_keywords(self) -> list[str]:
        return ["更新点", "当前批次进度", "下一步优先处理"]
