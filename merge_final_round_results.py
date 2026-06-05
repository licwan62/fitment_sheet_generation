from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


ROUND_RE = re.compile(r"^---\s*Round\s+(\d+)\s*/\s*(?:下一步|首次发送)\s*---\s*$")
RESULT_RE_TEMPLATE = r"^{base}_result(?:_(\d+))?\.md$"
PART_SUFFIX_RE = re.compile(r"_part_\d+$")
HEADER_ALIASES = {
    "年份": "年份区间",
    "货斗长度 (ft)": "货斗长度_ft",
    "状态": "迭代状态",
}


@dataclass
class ExtractedResult:
    source: Path
    round_number: int
    header: list[str]
    lines: list[str]


def version_number(path: Path, base: str) -> int:
    match = re.match(RESULT_RE_TEMPLATE.format(base=re.escape(base)), path.name)
    if not match:
        raise ValueError(f"not a result file for {base}: {path.name}")
    suffix = match.group(1)
    return int(suffix) if suffix else 1


def find_latest_result(results_dir: Path, base: str) -> Path | None:
    pattern = f"{base}_result*.md"
    candidates = [
        path
        for path in results_dir.glob(pattern)
        if re.match(RESULT_RE_TEMPLATE.format(base=re.escape(base)), path.name)
    ]
    if not candidates:
        return None
    return max(candidates, key=lambda path: version_number(path, base))


def extract_last_round(path: Path) -> ExtractedResult | None:
    text = path.read_text(encoding="utf-8-sig")
    lines = text.splitlines()
    round_indexes: list[tuple[int, int]] = []

    for index, line in enumerate(lines):
        match = ROUND_RE.match(line)
        if match:
            round_indexes.append((index, int(match.group(1))))

    if not round_indexes:
        return None

    def clean_content(content: list[str]) -> tuple[list[str], list[str]]:
        table_segments: list[tuple[list[str], list[str]]] = []
        current_header: list[str] | None = None
        current_rows: list[str] | None = None

        for line in content:
            stripped = line.strip()
            if not stripped:
                if current_header and current_rows:
                    table_segments.append((current_header, current_rows))
                current_header = None
                current_rows = None
                continue
            if stripped in {"本批次完成。", "本批次完成"}:
                continue
            if stripped.startswith("```"):
                continue
            if stripped.startswith("主车型\t"):
                if current_header and current_rows:
                    table_segments.append((current_header, current_rows))
                current_header = stripped.split("\t")
                current_rows = []
                continue
            if current_header is None or current_rows is None:
                continue
            if "\t" not in line:
                if current_rows:
                    table_segments.append((current_header, current_rows))
                current_header = None
                current_rows = None
                continue
            columns = line.rstrip("\r").split("\t")
            if len(columns) >= 2:
                current_rows.append(line.rstrip("\r"))
            elif current_rows:
                table_segments.append((current_header, current_rows))
                current_header = None
                current_rows = None

        if current_header and current_rows:
            table_segments.append((current_header, current_rows))

        return table_segments[-1] if table_segments else ([], [])

    for position in range(len(round_indexes) - 1, -1, -1):
        start_index, round_number = round_indexes[position]
        end_index = round_indexes[position + 1][0] if position + 1 < len(round_indexes) else len(lines)
        header, cleaned = clean_content(lines[start_index + 1 : end_index])
        if cleaned:
            return ExtractedResult(source=path, round_number=round_number, header=header, lines=cleaned)

    start_index, round_number = round_indexes[-1]
    return ExtractedResult(source=path, round_number=round_number, header=[], lines=[])


def read_origin_header(origin_files: list[Path]) -> list[str]:
    for origin_file in origin_files:
        for line in origin_file.read_text(encoding="utf-8-sig").splitlines():
            if line.strip():
                return line.rstrip("\r").split("\t")
    return []


def normalize_header_name(name: str) -> str:
    return HEADER_ALIASES.get(name.strip(), name.strip())


def align_result_line(result_header: list[str], output_header: list[str], line: str) -> str:
    values = line.rstrip("\r").split("\t")
    normalized_result_header = [normalize_header_name(name) for name in result_header]
    row_by_header = {
        header: values[index] if index < len(values) else ""
        for index, header in enumerate(normalized_result_header)
    }
    return "\t".join(row_by_header.get(header, "") for header in output_header)


def sort_key(path: Path) -> tuple:
    parts = re.split(r"(\d+)", path.stem)
    return tuple(int(part) if part.isdigit() else part for part in parts)


def merged_basename(origin_files: list[Path]) -> str:
    if not origin_files:
        return "merged"
    base = PART_SUFFIX_RE.sub("", origin_files[0].stem)
    return base or origin_files[0].stem


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    default_origin_dir = script_dir / "input_sheets"
    default_results_dir = script_dir / "output_sheets"
    default_output_dir = script_dir / "output_merged"
    default_log_dir = script_dir / "output_merged"

    parser = argparse.ArgumentParser(
        description="Merge the last Round / 下一步 section from the latest result markdown for each origin TSV."
    )
    parser.add_argument("--origin-dir", type=Path, default=default_origin_dir)
    parser.add_argument("--results-dir", type=Path, default=default_results_dir)
    parser.add_argument("--output-dir", type=Path, default=default_output_dir)
    parser.add_argument("--log-dir", type=Path, default=default_log_dir)
    parser.add_argument("--output", type=Path, help="Optional explicit merged TSV output path.")
    parser.add_argument("--log", type=Path, help="Optional explicit log output path.")
    parser.add_argument("--no-header", action="store_true", help="Do not write the merged TSV header row.")
    args = parser.parse_args()

    origin_dir = args.origin_dir.resolve()
    results_dir = args.results_dir.resolve()
    output_dir = args.output_dir.resolve()
    log_dir = args.log_dir.resolve()

    if not origin_dir.exists():
        raise FileNotFoundError(f"origin dir not found: {origin_dir}")
    if not results_dir.exists():
        raise FileNotFoundError(f"results dir not found: {results_dir}")

    origin_files = sorted(origin_dir.glob("*.tsv"), key=sort_key)
    origin_header = read_origin_header(origin_files)
    output_stem = merged_basename(origin_files)
    output_path = args.output.resolve() if args.output else (output_dir / f"{output_stem}_merged.tsv").resolve()
    log_path = args.log.resolve() if args.log else (log_dir / f"{output_stem}_merged.log").resolve()

    merged_lines: list[str] = []
    log_lines: list[str] = []

    if not args.no_header:
        merged_lines.append("\t".join(["来源文件", *origin_header]))
        log_lines.append(f"HEADER\torigin-dir\t{origin_header and origin_files[0].name or '(none)'}")

    stats = {"origin": len(origin_files), "merged_files": 0, "missing": 0, "no_round": 0, "rows": 0}

    for origin_file in origin_files:
        base = origin_file.stem
        latest_result = find_latest_result(results_dir, base)
        if latest_result is None:
            stats["missing"] += 1
            log_lines.append(f"MISSING\t{base}\t(no result md)")
            continue

        extracted = extract_last_round(latest_result)
        if extracted is None:
            stats["no_round"] += 1
            log_lines.append(f"NO_ROUND\t{base}\t{latest_result.name}")
            continue

        if extracted.lines:
            merged_lines.extend(
                f"{latest_result.name}\t{align_result_line(extracted.header, origin_header, line)}"
                for line in extracted.lines
            )
            stats["rows"] += len(extracted.lines)
            stats["merged_files"] += 1
            log_lines.append(
                f"MERGED\t{base}\t{latest_result.name}\tRound {extracted.round_number}\t{len(extracted.lines)} rows"
            )
        else:
            log_lines.append(f"EMPTY_ROUND\t{base}\t{latest_result.name}\tRound {extracted.round_number}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(merged_lines) + ("\n" if merged_lines else ""), encoding="utf-8")
    log_path.write_text("\n".join(log_lines) + ("\n" if log_lines else ""), encoding="utf-8")

    print(f"origin files: {stats['origin']}")
    print(f"merged files: {stats['merged_files']}")
    print(f"merged rows: {stats['rows']}")
    print(f"missing result md: {stats['missing']}")
    print(f"no round marker: {stats['no_round']}")
    print(f"output: {output_path}")
    print(f"log: {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
