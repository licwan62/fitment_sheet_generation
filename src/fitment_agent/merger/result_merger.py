"""Result merger — combines shard results into a single TSV.

Port of merge_final_round_results.py into the fitment_agent package.
"""

from __future__ import annotations

import re
from pathlib import Path


def merge_results(
    output_dir: Path,
    output_path: Path,
    *,
    expected_columns: list[str] | None = None,
    auto_empty_columns: list[str] | None = None,
) -> Path:
    """Merge all shard result files into a single TSV.

    For each shard result markdown file:
    1. Find the last round section
    2. Extract the TSV code block
    3. Align columns to the expected header
    4. Blank out auto-empty columns

    Returns the output path.
    """
    result_files = sorted(output_dir.glob("*_result.md"))
    if not result_files:
        raise FileNotFoundError(f"No result files found in {output_dir}")

    all_rows: list[str] = []
    header: str | None = None

    for result_file in result_files:
        content = result_file.read_text(encoding="utf-8")
        last_round_tsv = _extract_last_round_tsv(content)
        if not last_round_tsv:
            continue

        lines = last_round_tsv.strip().splitlines()
        if not lines:
            continue

        if header is None:
            header = lines[0]
            all_rows.append(header)

        # Add data rows (skip header)
        for line in lines[1:]:
            if line.strip() and "\t" in line:
                if auto_empty_columns and expected_columns:
                    line = _blank_auto_empty(
                        line, expected_columns, auto_empty_columns
                    )
                all_rows.append(line)

    if not all_rows:
        raise ValueError("No TSV data found in result files")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(all_rows), encoding="utf-8")
    return output_path


def _extract_last_round_tsv(content: str) -> str | None:
    """Extract the TSV code block from the last round section."""
    # Find all round sections
    round_pattern = re.compile(r"--- Round \d+.*?---", re.DOTALL)
    sections = list(round_pattern.finditer(content))

    if not sections:
        # No round markers — try to find any TSV block
        return _extract_last_tsv_block(content)

    # Get the last section's content
    last_start = sections[-1].end()
    last_section = content[last_start:]
    return _extract_last_tsv_block(last_section)


def _extract_last_tsv_block(text: str) -> str | None:
    """Extract the last TSV code block from text."""
    # Find all code blocks
    blocks = re.findall(r"```(?:tsv)?\s*\n(.*?)```", text, re.DOTALL)
    if not blocks:
        return None
    return blocks[-1]  # Return the last block


def _blank_auto_empty(
    line: str, columns: list[str], auto_empty: list[str]
) -> str:
    """Blank out auto-empty columns in a TSV row."""
    parts = line.split("\t")
    col_index = {name: i for i, name in enumerate(columns)}
    for col_name in auto_empty:
        idx = col_index.get(col_name)
        if idx is not None and idx < len(parts):
            parts[idx] = ""
    return "\t".join(parts)
