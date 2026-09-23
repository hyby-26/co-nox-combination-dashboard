from labels import display_name


def test_display_name_uses_conventional_nox_casing():
    assert display_name("NOX") == "NOx"


def test_display_name_passes_other_columns_through():
    for column in ["AT", "AP", "AH", "AFDP", "GTEP", "TIT", "TAT", "TEY", "CDP", "CO"]:
        assert display_name(column) == column
