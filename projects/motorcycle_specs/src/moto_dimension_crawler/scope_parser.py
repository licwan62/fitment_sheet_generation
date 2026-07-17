from __future__ import annotations


def width_scope(text: str) -> str:
    t = text.casefold()
    checks = [
        (("including mirrors", "with mirrors"), "WITH_MIRRORS"),
        (("excluding mirrors", "without mirrors"), "WITHOUT_MIRRORS"),
        (("handlebar",), "HANDLEBAR_WIDTH"),
        (("with panniers", "including panniers"), "WITH_PANNIERS"),
        (("without panniers",), "WITHOUT_PANNIERS"),
        (("side cases",), "WITH_SIDE_CASES"),
    ]
    return next((value for needles, value in checks if any(n in t for n in needles)), "UNKNOWN")


def height_scope(text: str) -> str:
    t = text.casefold()
    checks = [
        (("adjustable windscreen",), "ADJUSTABLE_WINDSCREEN"),
        (("windscreen high", "high screen"), "WINDSCREEN_HIGH"),
        (("windscreen low", "low screen"), "WINDSCREEN_LOW"),
        (("without windscreen",), "WITHOUT_WINDSCREEN"),
        (("with windscreen", "including windscreen"), "WITH_WINDSCREEN"),
        (("without mirrors",), "WITHOUT_MIRRORS"),
        (("with mirrors", "including mirrors"), "WITH_MIRRORS"),
    ]
    return next((value for needles, value in checks if any(n in t for n in needles)), "UNKNOWN")


def accessory_status(text: str) -> str:
    t = text.casefold()
    checks = [
        (("with panniers",), "WITH_PANNIERS"), (("top box",), "WITH_TOP_BOX"),
        (("side cases",), "WITH_SIDE_CASES"), (("touring package",), "TOURING_PACKAGE"),
        (("standard",), "STANDARD"),
    ]
    return next((value for needles, value in checks if any(n in t for n in needles)), "UNKNOWN")

