from __future__ import annotations

from pathlib import Path

import pandas as pd

from .models import InputRecord
from .normalizer import compact_name, normalize_name, number_tokens, word_tokens


def _read_delimited(path: Path) -> pd.DataFrame:
    sep = "\t" if path.suffix.lower() == ".tsv" else ","
    error: Exception | None = None
    for encoding in ("utf-8-sig", "utf-8", "gb18030"):
        try:
            return pd.read_csv(path, sep=sep, dtype=str, keep_default_na=False, encoding=encoding)
        except UnicodeDecodeError as exc:
            error = exc
    raise ValueError(f"Cannot decode {path}: {error}")


def read_input(path: Path, cfg: dict, sheet: str | None = None, start_row: int = 1, limit: int | None = None) -> list[InputRecord]:
    if path.suffix.lower() in {".xlsx", ".xls"}:
        df = pd.read_excel(path, sheet_name=sheet or 0, dtype=str, keep_default_na=False)
    elif path.suffix.lower() in {".csv", ".tsv"}:
        df = _read_delimited(path)
    else:
        raise ValueError("Input must be .xlsx, .csv or .tsv")
    mappings = cfg.get("input_columns", {})
    def find(kind: str, required: bool = True) -> str | None:
        for name in mappings.get(kind, []):
            if name in df.columns:
                return name
        if required:
            raise ValueError(f"Missing input column: {kind}")
        return None
    make_col, model_col, type_col = find("make"), find("model"), find("vehicle_type", False)
    start = max(0, start_row - 1)
    selected = df.iloc[start : start + limit if limit else None]
    records: list[InputRecord] = []
    for pos, (_, row) in enumerate(selected.iterrows(), start=start + 1):
        make, model = str(row[make_col]).strip(), str(row[model_col]).strip()
        rec = InputRecord(f"{pos:06d}", make, model, str(row[type_col]).strip() if type_col else "")
        rec.make_normalized = normalize_name(make)
        rec.model_normalized = normalize_name(model)
        rec.model_compact = compact_name(model)
        rec.number_tokens = number_tokens(model)
        rec.word_tokens = word_tokens(model)
        records.append(rec)
    return records
