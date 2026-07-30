from moto_dimension_crawler.year_parser import parse_year


def test_single_year():
    assert parse_year("BMW C 400 GT 2021") == ("2021", "2021", "2021")


def test_year_range():
    assert parse_year("2019–2021") == ("", "2019", "2021")


def test_unknown_year_is_blank():
    assert parse_year("BMW C 400 GT") == ("", "", "")
