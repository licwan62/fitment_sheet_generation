from __future__ import annotations

import re

from .models import DimensionResult
from .scope_parser import accessory_status, height_scope, width_scope


NUM = r"(\d+(?:\.\d+)?)"
UNIT = r"(mm|cm|in(?:ches)?|\")"
RANGE = rf"{NUM}\s*(?:-|–|—|to)\s*{NUM}\s*{UNIT}"
SINGLE = rf"{NUM}\s*{UNIT}"
LABELS = {
    "l": r"(?:overall\s+)?length",
    "w": r"(?<!tyre\s)(?<!tire\s)(?:overall\s+)?width",
    "h": r"(?<!seat\s)(?<!saddle\s)(?:overall\s+)?height",
    "wheelbase": r"wheel\s*base|wheelbase",
    "seat_height": r"seat\s*height",
    "ground_clearance": r"ground\s*clearance",
}


def to_mm(value: float, unit: str) -> float:
    unit = unit.casefold().rstrip("s")
    factor = 1 if unit == "mm" else 10 if unit == "cm" else 25.4
    return round(value * factor, 1)


def _put(result: DimensionResult, key: str, low: float, high: float, unit: str, raw: str) -> None:
    result.values[f"{key}_min"] = to_mm(low, unit)
    result.values[f"{key}_max"] = to_mm(high, unit)
    result.values[key] = result.values[f"{key}_max"]
    result.raw[key] = raw.strip()
    result.raw.setdefault("unit", unit)


def parse_dimensions(text: str) -> DimensionResult:
    clean = " ".join((text or "").replace("×", "x").split())
    clean = re.sub(r"(?<!\d)(\d)\s+(\d{2,3})(?=\s*(?:mm|cm|in(?:ches)?|\"))", r"\1\2", clean, flags=re.I)
    result = DimensionResult()
    snippets: list[str] = []
    # Combined L x W x H or slash form, unit at end.
    combo = re.search(rf"(?:dimensions?|length\s*/\s*width\s*/\s*height)\s*:?\s*{NUM}\s*(?:x|X|/)\s*{NUM}\s*(?:x|X|/)\s*{NUM}\s*{UNIT}", clean, re.I)
    if combo:
        vals, unit = [float(combo.group(i)) for i in range(1, 4)], combo.group(4)
        for key, val in zip(("l", "w", "h"), vals):
            _put(result, key, val, val, unit, combo.group(0))
        snippets.append(combo.group(0))
    for key, label in LABELS.items():
        # Label range takes precedence.
        found_range = re.search(rf"(?:{label})\s*:?\s*{RANGE}", clean, re.I)
        found = found_range or re.search(rf"(?:{label})\s*:?\s*{SINGLE}", clean, re.I)
        if not found:
            continue
        if found_range:
            low, high, unit = float(found.group(1)), float(found.group(2)), found.group(3)
        else:
            low = high = float(found.group(1)); unit = found.group(2)
        mapped = {"wheelbase":"wheelbase", "seat_height":"seat_height", "ground_clearance":"ground_clearance"}.get(key, key)
        _put(result, mapped, low, high, unit, found.group(0))
        snippets.append(found.group(0))
        dual = re.search(rf"(?:{label})\s*:?\s*{NUM}\s*{UNIT}\s*/\s*{NUM}\s*{UNIT}", clean, re.I)
        if dual:
            first = to_mm(float(dual.group(1)), dual.group(2))
            second = to_mm(float(dual.group(3)), dual.group(4))
            result.raw[mapped] = dual.group(0)
            snippets.append(dual.group(0))
            if abs(first - second) / max(first, second) > 0.05:
                result.anomaly_flags.append("UNIT_CONFLICT")
    main = [result.values.get(k) for k in ("l", "w", "h")]
    count = sum(v is not None for v in main)
    result.parse_status = "COMPLETE" if count == 3 else "PARTIAL" if count else "NO_DIMENSION"
    if "UNIT_CONFLICT" in result.anomaly_flags:
        result.parse_status = "UNIT_CONFLICT"
    result.dimension_raw = " | ".join(dict.fromkeys(snippets))
    context = " ".join(snippets)
    result.width_scope = width_scope(clean if result.values.get("w") is not None else context)
    result.height_scope = height_scope(clean if result.values.get("h") is not None else context)
    result.accessory_status = accessory_status(clean)
    return result
