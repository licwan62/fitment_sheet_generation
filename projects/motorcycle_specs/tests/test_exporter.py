from moto_dimension_crawler.exporter import build_fitment_rows


def test_fitment_view_prefers_complete_dimensions():
    inputs = [{"INPUT_ID":"000001","MAKE":"BMW","MODEL":"C400GT","车辆类型":"两轮摩托车"}]
    raw = [
        {"INPUT_ID":"000001","L-MM":2200,"W-MM":"","H-MM":1400,"MATCH_SCORE":95,"MATCH_CONFIDENCE":"HIGH","PARSE_STATUS":"PARTIAL","SOURCE_URL":"partial"},
        {"INPUT_ID":"000001","L-MM":2210,"W-MM":835,"H-MM":1437,"MATCH_SCORE":90,"MATCH_CONFIDENCE":"MEDIUM","PARSE_STATUS":"COMPLETE","SOURCE_URL":"complete"},
    ]
    row = build_fitment_rows(inputs, raw)[0]
    assert row["DIMENSION_STATUS"] == "FOUND_COMPLETE"
    assert row["SOURCE_URL"] == "complete"
    assert row["L-MM"] == 2210


def test_fitment_view_retains_not_found_input():
    row = build_fitment_rows([{"INPUT_ID":"000002","MAKE":"BMW","MODEL":"Unknown","车辆类型":""}], [])[0]
    assert row["DIMENSION_STATUS"] == "NOT_FOUND"
    assert row["L-MM"] is None
