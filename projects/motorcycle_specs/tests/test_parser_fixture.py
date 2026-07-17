from pathlib import Path

from moto_dimension_crawler.parser import parse_page


def test_local_html_fixture_parses_without_network():
    path = Path(__file__).parent / "fixtures" / "bmw_c400gt_2019.html"
    page = parse_page(path.read_text(encoding="utf-8"), "https://example.invalid/bmw-c400gt-2019.html")
    assert page["year"] == "2019"
    assert page["dimensions"].values["l"] == 2210
    assert page["dimensions"].values["h"] == 1437
    assert page["dimensions"].width_scope == "WITHOUT_MIRRORS"
