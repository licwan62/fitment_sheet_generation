"""Vehicle expansion — converts (make, model) into seed TSV rows.

Uses a lightweight LLM call to determine generations, year ranges,
body styles, cab types, and bed lengths for each vehicle.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from ..config.models import VehicleEntry
from ..llm.protocol import LLMBackend
from ..templates.base import RequirementTemplate


@dataclass
class ExpandedVehicle:
    """One row in the seed TSV, expanded from a (make, model) entry."""

    make: str
    model: str
    generation: str
    year_range: str
    body_style: str
    sub_version: str
    cab_type: str
    bed_length_ft: str
    category: str
    notes: str


class VehicleExpander:
    """Expands vehicle entries into a seed TSV using a preliminary LLM call."""

    def __init__(
        self,
        *,
        backend_factory: Callable[[], LLMBackend],
        template: RequirementTemplate,
    ) -> None:
        self._backend_factory = backend_factory
        self._template = template

    async def expand_to_tsv(self, vehicles: list[VehicleEntry]) -> str:
        """Expand all vehicle entries and return a complete seed TSV string."""
        all_rows: list[ExpandedVehicle] = []
        for entry in vehicles:
            rows = await self._expand_one(entry)
            all_rows.extend(rows)
        return self._build_tsv(all_rows)

    async def _expand_one(self, entry: VehicleEntry) -> list[ExpandedVehicle]:
        """Use an LLM call to expand one (make, model) into multiple rows."""
        backend = self._backend_factory()
        try:
            await backend.start_conversation()

            prompt = self._build_expansion_prompt(entry)
            await backend.send_message(prompt)
            reply = await backend.wait_for_reply()
            return self._parse_expansion_reply(reply.text, entry)
        finally:
            await backend.close()

    def _build_expansion_prompt(self, entry: VehicleEntry) -> str:
        constraints = []
        if entry.year_from:
            constraints.append(f"year_from={entry.year_from}")
        if entry.year_to:
            constraints.append(f"year_to={entry.year_to}")
        if entry.body_styles:
            constraints.append(f"body_styles={','.join(entry.body_styles)}")
        if entry.generations:
            constraints.append(f"generations={','.join(entry.generations)}")
        constraint_str = f"\nConstraints: {', '.join(constraints)}" if constraints else ""

        return (
            f"For the vehicle **{entry.make} {entry.model}**, list ALL generations, "
            f"year ranges, body styles, and (for pickups) cab types and bed lengths.{constraint_str}\n\n"
            f"Output as TSV with these exact columns:\n"
            f"Make\tModel\tGeneration\tYearRange\tBodyStyle\tSubVersion\tCabType\tBedLengthFt\tCategory\n\n"
            f"Rules:\n"
            f"- One row per unique combination of generation + year_range + body_style + cab_type + bed_length\n"
            f"- YearRange format: 'YYYY' or 'YYYY-YYYY'\n"
            f"- Generation: 'gen1', 'gen2', etc.\n"
            f"- CabType: 'Regular Cab', 'Extended Cab', 'Crew Cab' (pickups only, empty for others)\n"
            f"- BedLengthFt: numeric in feet (pickups only, empty for others)\n"
            f"- Category: Chinese category name (皮卡, SUV, 轿车, MPV, etc.)\n"
            f"- Include ALL years from first production to current/latest\n"
            f"- Do NOT include any header row in the output\n"
        )

    def _parse_expansion_reply(
        self, reply: str, entry: VehicleEntry
    ) -> list[ExpandedVehicle]:
        """Parse the LLM's TSV reply into ExpandedVehicle objects."""
        rows: list[ExpandedVehicle] = []
        in_block = False
        for line in reply.splitlines():
            stripped = line.strip()
            if stripped.startswith("```"):
                in_block = not in_block
                continue
            if not in_block or not stripped or "\t" not in stripped:
                continue

            parts = stripped.split("\t")
            if len(parts) < 9:
                parts.extend([""] * (9 - len(parts)))

            rows.append(
                ExpandedVehicle(
                    make=parts[0] or entry.make,
                    model=parts[1] or entry.model,
                    generation=parts[2],
                    year_range=parts[3],
                    body_style=parts[4],
                    sub_version=parts[5],
                    cab_type=parts[6],
                    bed_length_ft=parts[7],
                    category=parts[8],
                    notes=entry.notes or "",
                )
            )
        return rows

    @staticmethod
    def _build_tsv(rows: list[ExpandedVehicle]) -> str:
        """Convert expanded vehicles into the standard TSV format."""
        header = (
            "主车型\t分类\t品牌\t车型名\t结构\t版本\t代际\t年份区间\t"
            "驾驶室类型\t货斗长度_ft\tmax_length_in\tmax_width_in\tmax_height_in\t"
            "参考车型\t备注\t迭代状态"
        )
        lines = [header]
        for r in rows:
            main_model = f"{r.make} {r.model}"
            lines.append(
                f"{main_model}\t{r.category}\t{r.make}\t{r.model}\t"
                f"{r.body_style}\t{r.sub_version}\t{r.generation}\t{r.year_range}\t"
                f"{r.cab_type}\t{r.bed_length_ft}\t\t\t\t\t{r.notes}\t待补强"
            )
        return "\n".join(lines)
