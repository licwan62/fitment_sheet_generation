from moto_dimension_crawler.dimension_parser import parse_dimensions
from moto_dimension_crawler.validator import validate


CFG = {"validation":{"length_min_mm":900,"length_max_mm":3500,"width_min_mm":300,"width_max_mm":2000,"height_min_mm":400,"height_max_mm":2500}}


def test_out_of_range_is_flagged_not_deleted():
    result = validate(parse_dimensions("Length 5000 mm"), CFG)
    assert result.values["l"] == 5000
    assert "OUT_OF_RANGE" in result.anomaly_flags
    assert result.parse_status == "INVALID_VALUE"


def test_wheelbase_logic():
    result = validate(parse_dimensions("Length 2000 mm Wheelbase 2200 mm"), CFG)
    assert "WHEELBASE_GREATER_THAN_LENGTH" in result.anomaly_flags
