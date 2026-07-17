from __future__ import annotations

from .models import DimensionResult


def validate(result: DimensionResult, cfg: dict) -> DimensionResult:
    limits = cfg["validation"]
    for key, low_name, high_name in (("l", "length_min_mm", "length_max_mm"), ("w", "width_min_mm", "width_max_mm"), ("h", "height_min_mm", "height_max_mm")):
        value = result.values.get(key)
        if value is not None and not limits[low_name] <= value <= limits[high_name]:
            result.anomaly_flags.append("OUT_OF_RANGE")
    if result.values.get("h") is not None and result.values.get("seat_height") is not None and result.values["h"] < result.values["seat_height"]:
        result.anomaly_flags.append("HEIGHT_LOWER_THAN_SEAT_HEIGHT")
    if result.values.get("wheelbase") is not None and result.values.get("l") is not None and result.values["wheelbase"] > result.values["l"]:
        result.anomaly_flags.append("WHEELBASE_GREATER_THAN_LENGTH")
    if "OUT_OF_RANGE" in result.anomaly_flags or any(x.endswith("HEIGHT") or x.endswith("LENGTH") for x in result.anomaly_flags):
        result.parse_status = "INVALID_VALUE"
    return result
