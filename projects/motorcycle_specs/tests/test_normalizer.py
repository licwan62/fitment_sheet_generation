import pytest

from moto_dimension_crawler.normalizer import equivalent, normalize_name


@pytest.mark.parametrize("left,right", [
    ("C400GT", "C 400 GT"), ("C evolution", "C Evolution"), ("R1250GS", "R 1250 GS"),
    ("MT07", "MT-07"), ("CBR1000RR-R", "CBR 1000 RR-R"),
])
def test_equivalent_names(left, right):
    assert equivalent(left, right)


def test_unicode_and_spacing():
    assert normalize_name("  Ｃ400ＧＴ ") == "c 400 gt"
