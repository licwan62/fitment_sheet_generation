from __future__ import annotations

from collections import defaultdict

from .normalizer import compact_name


def group_dimensions(rows: list[dict], cfg: dict) -> list[dict]:
    tolerances = cfg["dimension"]["group_tolerance_mm"]
    by_input: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in rows:
        if row.get("MATCH_STATUS") in {"EXACT", "LIKELY", "MULTIPLE"} and any(row.get(k) not in (None, "") for k in ("L-MM", "W-MM", "H-MM")):
            by_input[(row["MAKE"], row["MODEL"])].append(row)
    output: list[dict] = []
    for (make, model), items in by_input.items():
        groups: list[list[dict]] = []
        for item in items:
            placed = False
            for group in groups:
                ref = group[0]
                compatible = all(
                    item.get(field) is not None and ref.get(field) is not None and abs(float(item[field]) - float(ref[field])) <= tolerances[key]
                    for field, key in (("L-MM", "length"), ("W-MM", "width"), ("H-MM", "height"))
                ) and item.get("WIDTH_SCOPE") == ref.get("WIDTH_SCOPE") and item.get("HEIGHT_SCOPE") == ref.get("HEIGHT_SCOPE") and item.get("ACCESSORY_STATUS") == ref.get("ACCESSORY_STATUS")
                if compatible:
                    group.append(item); placed = True; break
            if not placed:
                groups.append([item])
        for number, group in enumerate(groups, 1):
            ref = group[0]
            years = sorted({str(x.get("YEAR")) for x in group if x.get("YEAR")})
            starts = [int(x["YEAR_START"]) for x in group if str(x.get("YEAR_START", "")).isdigit()]
            ends = [int(x["YEAR_END"]) for x in group if str(x.get("YEAR_END", "")).isdigit()]
            output.append({
                "DIMENSION_GROUP_ID": f"MOTO-DIM-{compact_name(make).upper()}-{compact_name(model).upper()}-{number:04d}",
                "MAKE": make, "MODEL": model, "VERSION": ref.get("SOURCE_VERSION", ""), "YEARS": ",".join(years),
                "YEAR_START": min(starts) if starts and years and len(years) == max(ends)-min(starts)+1 else "",
                "YEAR_END": max(ends) if ends and years and len(years) == max(ends)-min(starts)+1 else "",
                "L-MM": ref.get("L-MM"), "W-MM": ref.get("W-MM"), "H-MM-MIN": ref.get("H-MM-MIN"), "H-MM-MAX": ref.get("H-MM-MAX"),
                "WIDTH_SCOPE": ref.get("WIDTH_SCOPE"), "HEIGHT_SCOPE": ref.get("HEIGHT_SCOPE"), "ACCESSORY_STATUS": ref.get("ACCESSORY_STATUS"),
                "SOURCE_COUNT": len(group), "SOURCE_URLS": " | ".join(x["SOURCE_URL"] for x in group),
                "CONFIDENCE": min((x.get("CONFIDENCE", "LOW") for x in group), key=lambda x: {"LOW":0,"MEDIUM":1,"HIGH":2}.get(x,0)),
                "REVIEW_STATUS": "REVIEW" if any(x.get("CONFIDENCE") != "HIGH" for x in group) else "CONFIRMED",
            })
    return output
