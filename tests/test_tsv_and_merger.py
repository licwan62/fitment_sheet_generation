"""Tests for TSV splitter and result merger."""

import textwrap
from pathlib import Path

import pytest

from fitment_agent.vehicle.tsv_splitter import split_tsv, audit_split
from fitment_agent.merger.result_merger import (
    merge_results,
    _extract_last_round_tsv,
    _extract_last_tsv_block,
)


# ---------------------------------------------------------------------------
# TSV Splitter
# ---------------------------------------------------------------------------

SAMPLE_TSV = "header\tcol1\tcol2\n" + "\n".join(
    f"row{i}\tval{i}a\tval{i}b" for i in range(1, 11)
)


class TestSplitTsv:
    def test_basic_split(self, tmp_path):
        shards = split_tsv(SAMPLE_TSV, chunk_size=3, output_dir=tmp_path)
        assert len(shards) == 4  # ceil(10/3) = 4
        for name, content in shards:
            lines = content.strip().splitlines()
            assert lines[0] == "header\tcol1\tcol2"  # header preserved
            assert len(lines) <= 4  # header + max 3 data rows

    def test_single_shard(self, tmp_path):
        shards = split_tsv(SAMPLE_TSV, chunk_size=100, output_dir=tmp_path)
        assert len(shards) == 1
        lines = shards[0][1].strip().splitlines()
        assert len(lines) == 11  # header + 10 data rows

    def test_exact_fit(self, tmp_path):
        shards = split_tsv(SAMPLE_TSV, chunk_size=5, output_dir=tmp_path)
        assert len(shards) == 2
        assert len(shards[0][1].strip().splitlines()) == 6  # header + 5
        assert len(shards[1][1].strip().splitlines()) == 6  # header + 5

    def test_files_written(self, tmp_path):
        shards = split_tsv(SAMPLE_TSV, chunk_size=3, output_dir=tmp_path)
        for name, _ in shards:
            assert (tmp_path / f"{name}.tsv").exists()

    def test_empty_content(self, tmp_path):
        shards = split_tsv("", chunk_size=5, output_dir=tmp_path)
        assert shards == []

    def test_header_only(self, tmp_path):
        shards = split_tsv("header\tcol1", chunk_size=5, output_dir=tmp_path)
        assert shards == []


class TestAuditSplit:
    def test_complete(self, tmp_path):
        shards = split_tsv(SAMPLE_TSV, chunk_size=3, output_dir=tmp_path)
        assert audit_split(SAMPLE_TSV, shards) is True


# ---------------------------------------------------------------------------
# Result Merger helpers
# ---------------------------------------------------------------------------

class TestExtractLastTsvBlock:
    def test_single_block(self):
        text = "Some text\n```\nheader\tcol\nval1\tval2\n```"
        result = _extract_last_tsv_block(text)
        assert "header\tcol" in result
        assert "val1\tval2" in result

    def test_multiple_blocks(self):
        text = (
            "```\nold\tdata\n```\n"
            "middle text\n"
            "```\nnew\tdata\n```"
        )
        result = _extract_last_tsv_block(text)
        assert "new\tdata" in result

    def test_no_block(self):
        assert _extract_last_tsv_block("no code blocks here") is None


class TestExtractLastRoundTsv:
    def test_last_round(self):
        content = textwrap.dedent("""\
            --- Round 1 ---

            Some analysis...
            ```
            header\tcol
            row1\tval1
            ```

            --- Round 2 ---

            Final data:
            ```
            header\tcol
            row1\tval1_updated
            row2\tval2
            ```
        """)
        result = _extract_last_round_tsv(content)
        assert result is not None
        assert "row1\tval1_updated" in result

    def test_no_round_markers(self):
        content = "```\nheader\tcol\nrow1\tval1\n```"
        result = _extract_last_round_tsv(content)
        assert result is not None
        assert "row1\tval1" in result


class TestMergeResults:
    def test_merge(self, tmp_path):
        output_dir = tmp_path / "output"
        output_dir.mkdir()
        (output_dir / "part_01_result.md").write_text(
            "--- Round 1 ---\n\n```\nheader\tcol\nrow1\tval1\n```\n",
            encoding="utf-8",
        )
        (output_dir / "part_02_result.md").write_text(
            "--- Round 1 ---\n\n```\nheader\tcol\nrow2\tval2\n```\n",
            encoding="utf-8",
        )
        out_path = tmp_path / "merged.tsv"
        result = merge_results(output_dir, out_path)
        assert result.exists()
        content = result.read_text(encoding="utf-8")
        assert "header\tcol" in content
        assert "row1\tval1" in content
        assert "row2\tval2" in content

    def test_no_results(self, tmp_path):
        output_dir = tmp_path / "empty"
        output_dir.mkdir()
        with pytest.raises(FileNotFoundError):
            merge_results(output_dir, tmp_path / "out.tsv")
