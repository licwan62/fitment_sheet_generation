import pytest

from moto_dimension_crawler.dimension_parser import parse_dimensions


@pytest.mark.parametrize("text,expected", [
    ("Length 2200 mm Width 880 mm Height 1420 mm", (2200,880,1420)),
    ("Dimensions: 2200 x 880 x 1420 mm", (2200,880,1420)),
    ("Overall Length: 86.6 in Overall Width: 34.6 in Overall Height: 55.9 in", (2199.6,878.8,1419.9)),
])
def test_common_dimension_formats(text, expected):
    result = parse_dimensions(text)
    assert (result.values["l"], result.values["w"], result.values["h"]) == expected
    assert result.parse_status == "COMPLETE"


def test_height_range():
    result = parse_dimensions("Height: 1430-1470 mm")
    assert result.values["h_min"] == 1430
    assert result.values["h_max"] == result.values["h"] == 1470


def test_dual_unit_keeps_metric_raw():
    result = parse_dimensions("Length 2200 mm / 86.6 in")
    assert result.values["l"] == 2200
    assert "2200 mm" in result.raw["l"]


def test_conflicting_dual_units_are_flagged():
    result = parse_dimensions("Length 2200 mm / 80 in")
    assert result.values["l"] == 2200
    assert result.parse_status == "UNIT_CONFLICT"
    assert "UNIT_CONFLICT" in result.anomaly_flags


def test_scope_detection():
    result = parse_dimensions("Width 980 mm including mirrors Height 1430-1470 mm with adjustable windscreen")
    assert result.width_scope == "WITH_MIRRORS"
    assert result.height_scope == "ADJUSTABLE_WINDSCREEN"


def test_seat_height_is_not_overall_height():
    result = parse_dimensions("Seat height 775 mm Overall height 1437 mm")
    assert result.values["seat_height"] == 775
    assert result.values["h"] == 1437


def test_spaced_dimension_digits_from_html_text_are_joined():
    result = parse_dimensions("Dimensions Length 2 300 mm Width 9 39 mm Wheelbase 1 585 mm Seat Height 8 75 mm")
    assert result.values["l"] == 2300
    assert result.values["w"] == 939
    assert result.values["wheelbase"] == 1585
    assert result.values["seat_height"] == 875
