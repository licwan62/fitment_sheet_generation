"""TSV splitter — splits a large TSV into numbered shards.

Port of split_origin_tsv.py into the fitment_agent package.
"""

from __future__ import annotations

from pathlib import Path


def split_tsv(
    content: str,
    chunk_size: int,
    output_dir: Path,
    *,
    prefix: str = "split_part",
) -> list[tuple[str, str]]:
    """Split TSV content into chunks and write to output_dir.

    Returns a list of (shard_name, shard_content) tuples.
    Each shard includes the header row.
    """
    lines = content.strip().splitlines()
    if not lines:
        return []

    header = lines[0]
    data_lines = lines[1:]

    if not data_lines:
        return []

    # Calculate number of shards
    total = len(data_lines)
    num_shards = max(1, (total + chunk_size - 1) // chunk_size)

    output_dir.mkdir(parents=True, exist_ok=True)
    shards: list[tuple[str, str]] = []

    for i in range(num_shards):
        start = i * chunk_size
        end = min(start + chunk_size, total)
        chunk_lines = data_lines[start:end]
        shard_content = header + "\n" + "\n".join(chunk_lines)
        shard_name = f"{prefix}_{i + 1:02d}"

        shard_path = output_dir / f"{shard_name}.tsv"
        shard_path.write_text(shard_content, encoding="utf-8")
        shards.append((shard_name, shard_content))

    return shards


def audit_split(origin_content: str, shards: list[tuple[str, str]]) -> bool:
    """Verify that all origin rows are present in the shards (no duplicates, no gaps)."""
    origin_lines = origin_content.strip().splitlines()
    origin_data = set(origin_lines[1:])  # skip header

    shard_data: list[str] = []
    for _, shard_content in shards:
        shard_lines = shard_content.strip().splitlines()
        shard_data.extend(shard_lines[1:])  # skip header

    shard_set = set(shard_data)
    return origin_data == shard_set and len(shard_data) == len(origin_data)
