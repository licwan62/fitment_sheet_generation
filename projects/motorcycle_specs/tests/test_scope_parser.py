from moto_dimension_crawler.scope_parser import accessory_status, height_scope, width_scope


def test_scopes():
    assert width_scope("Width including mirrors") == "WITH_MIRRORS"
    assert width_scope("Width") == "UNKNOWN"
    assert height_scope("with adjustable windscreen") == "ADJUSTABLE_WINDSCREEN"
    assert accessory_status("touring package") == "TOURING_PACKAGE"
