from moto_dimension_crawler.grouper import group_dimensions


CFG = {"dimension":{"group_tolerance_mm":{"length":5,"width":5,"height":5}}}


def row(year, length=2200):
    return {"MAKE":"BMW","MODEL":"C400GT","MATCH_STATUS":"EXACT","YEAR":str(year),"YEAR_START":str(year),"YEAR_END":str(year),
        "L-MM":length,"W-MM":880,"H-MM":1420,"H-MM-MIN":1420,"H-MM-MAX":1420,"WIDTH_SCOPE":"UNKNOWN","HEIGHT_SCOPE":"UNKNOWN",
        "ACCESSORY_STATUS":"UNKNOWN","SOURCE_URL":f"https://example/{year}","CONFIDENCE":"MEDIUM"}


def test_close_dimensions_group_and_keep_discontinuous_years():
    groups = group_dimensions([row(2019), row(2020,2204), row(2024)], CFG)
    assert len(groups) == 1
    assert groups[0]["YEARS"] == "2019,2020,2024"
    assert groups[0]["YEAR_START"] == groups[0]["YEAR_END"] == ""
