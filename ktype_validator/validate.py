#!/usr/bin/env python3
"""Validate final Ktype mapping and dimension TSV files.

Only the Python standard library is used.  By default, workspace roots come
from config.yaml and are searched recursively.  RESULT_DIR can override them
for a one-directory validation run.
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable


REQUIRED_COLUMNS = {
    "source": {"Ktype"},
    "mapping": {"id", "Ktype", "DIMENSION_GROUP_ID", "IterationStatus"},
    "dimension": {
        "DIMENSION_GROUP_ID",
        "LengthMM",
        "WidthMM",
        "HeightMM",
    },
}
OUTPUT_COLUMNS = {
    "mapping": [
        "id",
        "Ktype",
        "NormalizedBodyStyle",
        "Generation",
        "BodyCode",
        "Doors",
        "DIMENSION_GROUP_ID",
        "MatchConfidence",
        "Notes",
        "IterationStatus",
    ],
    "dimension": [
        "DIMENSION_GROUP_ID",
        "LengthMM",
        "WidthMM",
        "HeightMM",
        "DimensionSource",
        "SourceURL",
    ],
}


class ValidationInputError(Exception):
    """Raised when configuration or an input file cannot be read."""


@dataclass
class ValidationResult:
    source_total: int = 0
    ready_total: int = 0
    missing_ktypes: list[str] = field(default_factory=list)
    mapping_rows: int = 0
    valid_references: int = 0
    missing_references: list[dict[str, str]] = field(default_factory=list)
    dimension_conflicts: dict[str, set[tuple[str, str, str]]] = field(
        default_factory=dict
    )
    mapping_conflicts: dict[str, set[tuple[str, ...]]] = field(default_factory=dict)
    mapping_files: list[str] = field(default_factory=list)
    dimension_files: list[str] = field(default_factory=list)
    skipped_files: list[str] = field(default_factory=list)
    iteration_rows: int = 0
    iteration_unmatched: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not (
            self.errors
            or self.missing_ktypes
            or self.missing_references
            or self.dimension_conflicts
            or self.mapping_conflicts
        )


def natural_key(value: str) -> tuple[int, int | str]:
    return (0, int(value)) if value.isdigit() else (1, value)


def load_config(path: Path) -> dict[str, Any]:
    """Read the small, fixed YAML subset used by this validator."""
    if not path.is_file():
        raise ValidationInputError(f"配置文件不存在: {path}")
    values: dict[str, str] = {}
    workspaces: list[str] = []
    iteration: dict[str, str] = {}
    section = ""
    for line_number, raw_line in enumerate(
        path.read_text(encoding="utf-8-sig").splitlines(), start=1
    ):
        line = raw_line.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip())
        stripped = line.strip()
        if indent == 0 and stripped.endswith(":"):
            section = stripped[:-1].strip()
            continue
        if indent > 0 and section == "files" and ":" in stripped:
            key, value = stripped.split(":", 1)
            value = value.strip().strip('"\'')
            if not value:
                raise ValidationInputError(
                    f"配置值为空: {path}:{line_number} ({key.strip()})"
                )
            values[key.strip()] = value
            continue
        if indent > 0 and section == "workspaces" and stripped.startswith("-"):
            value = stripped[1:].strip().strip('"\'')
            if not value:
                raise ValidationInputError(f"workspace 路径为空: {path}:{line_number}")
            workspaces.append(value)
            continue
        if indent > 0 and section == "iteration" and ":" in stripped:
            key, value = stripped.split(":", 1)
            value = value.strip().strip('"\'')
            if not value:
                raise ValidationInputError(
                    f"配置值为空: {path}:{line_number} ({key.strip()})"
                )
            iteration[key.strip()] = value
            continue
        raise ValidationInputError(f"不支持的配置格式: {path}:{line_number}")
    missing = sorted({"mapping", "dimension", "source"} - values.keys())
    if missing:
        raise ValidationInputError(f"配置缺少 files 字段: {', '.join(missing)}")
    if not workspaces:
        raise ValidationInputError("配置缺少 workspaces 列表")
    return {
        "files": values,
        "workspaces": workspaces,
        "iteration": {"output": iteration.get("output", "iteration_input.tsv")},
    }


def resolve_source_path(configured: str, config_path: Path) -> Path:
    path = Path(configured).expanduser()
    if path.is_absolute():
        return path
    candidates = [Path.cwd() / path, config_path.parent / path]
    script_repo_root = Path(__file__).resolve().parent.parent
    candidates.append(script_repo_root / path)
    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()
    return candidates[0].resolve()


def resolve_workspace_path(configured: str, config_path: Path) -> Path:
    path = Path(configured).expanduser()
    if path.is_absolute():
        return path
    candidates = [Path.cwd() / path, Path(__file__).resolve().parent.parent / path]
    candidates.append(config_path.parent / path)
    for candidate in candidates:
        if candidate.is_dir():
            return candidate.resolve()
    return candidates[0].resolve()


def discover_files(roots: Iterable[Path], exact_name: str) -> list[Path]:
    discovered: list[Path] = []
    for root in roots:
        discovered.extend(sorted(path.resolve() for path in root.rglob(exact_name) if path.is_file()))
    return discovered


def read_tsv(path: Path, kind: str) -> list[dict[str, str]]:
    try:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle, delimiter="\t")
            columns = set(reader.fieldnames or [])
            missing = sorted(REQUIRED_COLUMNS[kind] - columns)
            if missing:
                raise ValidationInputError(
                    f"{path} 缺少必需列: {', '.join(missing)}"
                )
            rows = []
            for row_number, row in enumerate(reader, start=2):
                if None in row:
                    raise ValidationInputError(
                        f"{path}:{row_number} 的字段数超过表头"
                    )
                rows.append({key: (value or "").strip() for key, value in row.items()})
            return rows
    except UnicodeDecodeError as error:
        raise ValidationInputError(f"{path} 不是有效 UTF-8 文件: {error}") from error
    except csv.Error as error:
        raise ValidationInputError(f"{path} TSV 解析失败: {error}") from error


def merge_by_key(
    paths: Iterable[Path], kind: str, key_column: str
) -> tuple[
    list[dict[str, str]],
    dict[str, set[tuple[str, ...]]],
    list[dict[str, str]],
    list[str],
]:
    """Merge in configured order; later rows replace earlier rows with the same key."""
    merged: dict[str, dict[str, str]] = {}
    signatures: dict[str, set[tuple[str, ...]]] = defaultdict(set)
    all_rows: list[dict[str, str]] = []
    skipped: list[str] = []
    columns = OUTPUT_COLUMNS[kind]
    for path in paths:
        try:
            file_rows = read_tsv(path, kind)
        except (OSError, ValidationInputError) as error:
            skipped.append(f"{path}: {error}")
            continue
        for row_number, row in enumerate(file_rows, start=2):
            key = row[key_column]
            if not key:
                raise ValidationInputError(f"{path}:{row_number} 的 {key_column} 为空")
            signature = tuple(row.get(column, "") for column in columns)
            signatures[key].add(signature)
            merged[key] = row
            all_rows.append(row)
    conflicts = {key: rows for key, rows in signatures.items() if len(rows) > 1}
    return list(merged.values()), conflicts, all_rows, skipped


def write_tsv(path: Path, kind: str, rows: Iterable[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=OUTPUT_COLUMNS[kind],
            delimiter="\t",
            lineterminator="\n",
            extrasaction="ignore",
        )
        writer.writeheader()
        writer.writerows(rows)


def write_iteration_input(
    source_path: Path, missing_ktypes: Iterable[str], output_path: Path
) -> tuple[int, list[str]]:
    """Join missing Ktypes back to the source TSV and preserve all source columns."""
    wanted = {value.strip() for value in missing_ktypes if value.strip()}
    found: set[str] = set()
    count = 0
    with source_path.open(encoding="utf-8-sig", newline="") as source_handle:
        reader = csv.DictReader(source_handle, delimiter="\t")
        if "Ktype" not in (reader.fieldnames or []):
            raise ValidationInputError(f"{source_path} 缺少必需列: Ktype")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8", newline="") as output_handle:
            writer = csv.DictWriter(
                output_handle,
                fieldnames=reader.fieldnames,
                delimiter="\t",
                lineterminator="\n",
                extrasaction="ignore",
            )
            writer.writeheader()
            for row in reader:
                ktype = (row.get("Ktype") or "").strip()
                if ktype not in wanted:
                    continue
                writer.writerow(row)
                found.add(ktype)
                count += 1
    return count, sorted(wanted - found, key=natural_key)


def validate_tables(
    source_rows: Iterable[dict[str, str]],
    mapping_rows: list[dict[str, str]],
    dimension_rows: Iterable[dict[str, str]],
    mapping_conflicts: dict[str, set[tuple[str, ...]]] | None = None,
) -> ValidationResult:
    result = ValidationResult(mapping_rows=len(mapping_rows))
    result.mapping_conflicts = mapping_conflicts or {}
    source_ktypes = {row["Ktype"] for row in source_rows if row["Ktype"]}
    result.source_total = len(source_ktypes)

    statuses_by_ktype: dict[str, list[str]] = defaultdict(list)
    for row in mapping_rows:
        if row["Ktype"]:
            statuses_by_ktype[row["Ktype"]].append(row["IterationStatus"].upper())
    ready_ktypes = {
        ktype
        for ktype, statuses in statuses_by_ktype.items()
        if statuses and all(status == "READY" for status in statuses)
    }
    result.ready_total = len(source_ktypes & ready_ktypes)
    result.missing_ktypes = sorted(source_ktypes - ready_ktypes, key=natural_key)

    dimensions_by_id: dict[str, set[tuple[str, str, str]]] = defaultdict(set)
    for row in dimension_rows:
        group_id = row["DIMENSION_GROUP_ID"]
        if group_id:
            dimensions_by_id[group_id].add(
                (row["LengthMM"], row["WidthMM"], row["HeightMM"])
            )
    result.dimension_conflicts = {
        group_id: sizes
        for group_id, sizes in dimensions_by_id.items()
        if len(sizes) > 1
    }

    known_dimension_ids = set(dimensions_by_id)
    for row_number, row in enumerate(mapping_rows, start=2):
        group_id = row["DIMENSION_GROUP_ID"]
        if group_id and group_id in known_dimension_ids:
            result.valid_references += 1
        else:
            result.missing_references.append(
                {
                    "row": str(row_number),
                    "id": row["id"],
                    "Ktype": row["Ktype"],
                    "DIMENSION_GROUP_ID": group_id,
                }
            )
    return result


def write_lines(path: Path, lines: Iterable[str]) -> None:
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_outputs(result: ValidationResult, report_dir: Path) -> None:
    report_dir.mkdir(parents=True, exist_ok=True)
    write_lines(report_dir / "missing_ktype.txt", result.missing_ktypes)

    missing_dimension_lines = ["row\tid\tKtype\tDIMENSION_GROUP_ID"]
    missing_dimension_lines.extend(
        "\t".join(
            (item["row"], item["id"], item["Ktype"], item["DIMENSION_GROUP_ID"])
        )
        for item in result.missing_references
    )
    write_lines(report_dir / "missing_dimension.txt", missing_dimension_lines)

    conflict_lines: list[str] = []
    for group_id in sorted(result.dimension_conflicts):
        conflict_lines.append(group_id)
        for sizes in sorted(result.dimension_conflicts[group_id]):
            conflict_lines.append("\t".join(sizes))
        conflict_lines.append("")
    write_lines(report_dir / "dimension_conflict.txt", conflict_lines)

    mapping_conflict_lines: list[str] = []
    for mapping_id in sorted(result.mapping_conflicts, key=natural_key):
        mapping_conflict_lines.append(mapping_id)
        for row in sorted(result.mapping_conflicts[mapping_id]):
            mapping_conflict_lines.append("\t".join(row))
        mapping_conflict_lines.append("")
    write_lines(report_dir / "mapping_conflict.txt", mapping_conflict_lines)

    discovered_lines = ["[mapping]"] + result.mapping_files
    discovered_lines += ["", "[dimension]"] + result.dimension_files
    write_lines(report_dir / "discovered_files.txt", discovered_lines)
    write_lines(report_dir / "skipped_files.txt", result.skipped_files)

    file_status = "PASS" if not result.errors else "FAILED"
    reference_status = "PASS" if not result.missing_references else "FAILED"
    conflict_status = "PASS" if not result.dimension_conflicts else "FAILED"
    mapping_conflict_status = "PASS" if not result.mapping_conflicts else "FAILED"
    final_status = "PASS" if result.passed else "FAILED"
    error_section = ""
    if result.errors:
        error_section = "\n\nInput Errors\n\n" + "\n".join(
            f"- {error}" for error in result.errors
        )
    report = f"""========================
Ktype Validation Report
========================


Ktype Coverage

TOTAL:
{result.source_total}

READY:
{result.ready_total}

PENDING:
{len(result.missing_ktypes)}


Discovered Files

MAPPING FILES:
{len(result.mapping_files)}

DIMENSION FILES:
{len(result.dimension_files)}

SKIPPED FILES:
{len(result.skipped_files)}

{file_status}


Iteration Input

SOURCE ROWS:
{result.iteration_rows}

UNMATCHED KTYPES:
{len(result.iteration_unmatched)}


Dimension Reference

TOTAL MAPPING:
{result.mapping_rows}

VALID:
{result.valid_references}

MISSING DIMENSION:
{len(result.missing_references)}

{reference_status}


Dimension Conflict

CONFLICT GROUPS:
{len(result.dimension_conflicts)}

{conflict_status}


Mapping Merge Conflict

CONFLICT IDS:
{len(result.mapping_conflicts)}

{mapping_conflict_status}{error_section}


FINAL STATUS:

{final_status}
"""
    (report_dir / "validation_report.txt").write_text(report, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    script_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "result_dir",
        nargs="?",
        type=Path,
        default=None,
        help="可选：只递归检查该目录；默认使用 config.yaml 的 workspaces",
    )
    parser.add_argument(
        "--config", type=Path, default=script_dir / "config.yaml", help="配置文件"
    )
    parser.add_argument(
        "--report-dir", type=Path, default=script_dir / "report", help="报告目录"
    )
    args = parser.parse_args(argv)

    result = ValidationResult()
    try:
        config_path = args.config.resolve()
        config = load_config(config_path)
        files = config["files"]
        roots = [args.result_dir.resolve()] if args.result_dir else [
            resolve_workspace_path(item, config_path) for item in config["workspaces"]
        ]
        missing_roots = [str(root) for root in roots if not root.is_dir()]
        if missing_roots:
            raise ValidationInputError(f"workspace 目录不存在: {', '.join(missing_roots)}")
        source_path = resolve_source_path(files["source"], config_path)
        if not source_path.is_file():
            raise ValidationInputError(f"源文件不存在: {source_path}")
        mapping_paths = discover_files(roots, files["mapping"])
        dimension_paths = discover_files(roots, files["dimension"])
        if not mapping_paths:
            raise ValidationInputError(f"未递归找到文件: {files['mapping']}")
        if not dimension_paths:
            raise ValidationInputError(f"未递归找到文件: {files['dimension']}")

        merged_mappings, mapping_conflicts, _, skipped_mappings = merge_by_key(
            mapping_paths, "mapping", "id"
        )
        merged_dimensions, _, all_dimensions, skipped_dimensions = merge_by_key(
            dimension_paths, "dimension", "DIMENSION_GROUP_ID"
        )
        if not merged_mappings:
            raise ValidationInputError("没有可合并的有效 mapping 记录")
        if not merged_dimensions:
            raise ValidationInputError("没有可合并的有效 dimension 记录")
        result = validate_tables(
            read_tsv(source_path, "source"),
            merged_mappings,
            all_dimensions,
            mapping_conflicts,
        )
        result.mapping_files = [str(path) for path in mapping_paths]
        result.dimension_files = [str(path) for path in dimension_paths]
        result.skipped_files = skipped_mappings + skipped_dimensions
        result.errors.extend(f"已跳过不兼容文件: {item}" for item in result.skipped_files)
        report_dir = args.report_dir.resolve()
        report_dir.mkdir(parents=True, exist_ok=True)
        write_tsv(report_dir / "merged_ktype_mapping_final.tsv", "mapping", merged_mappings)
        write_tsv(
            report_dir / "merged_dimension_groups_final.tsv", "dimension", merged_dimensions
        )
        iteration_name = config["iteration"]["output"]
        result.iteration_rows, result.iteration_unmatched = write_iteration_input(
            source_path, result.missing_ktypes, report_dir / iteration_name
        )
        if result.iteration_unmatched:
            result.errors.append(
                "missing Ktype 无法回查源表: " + ",".join(result.iteration_unmatched)
            )
    except (OSError, ValidationInputError) as error:
        result.errors.append(str(error))

    try:
        write_outputs(result, args.report_dir.resolve())
    except OSError as error:
        print(f"无法写入报告: {error}", file=sys.stderr)
        return 2

    report_path = args.report_dir.resolve() / "validation_report.txt"
    print(f"validation report: {report_path}")
    print(f"FINAL STATUS: {'PASS' if result.passed else 'FAILED'}")
    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
