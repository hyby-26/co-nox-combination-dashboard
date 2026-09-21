import pandas as pd

from data_loader import load_data, get_years, get_sensor_columns


def test_load_data_returns_expected_columns():
    df = load_data()
    assert list(df.columns) == [
        "datetime", "AT", "AP", "AH", "AFDP", "GTEP",
        "TIT", "TAT", "TEY", "CDP", "CO", "NOX",
    ]


def test_load_data_returns_expected_row_count():
    df = load_data()
    assert len(df) == 36733


def test_load_data_parses_datetime_column():
    df = load_data()
    assert pd.api.types.is_datetime64_any_dtype(df["datetime"])


def test_load_data_is_cached_across_calls():
    df1 = load_data()
    df2 = load_data()
    assert df1 is df2


def test_get_years_returns_sorted_unique_years():
    df = pd.DataFrame({
        "datetime": pd.to_datetime(["2012-01-01", "2011-01-01", "2011-06-01"]),
    })
    assert get_years(df) == [2011, 2012]


def test_get_sensor_columns_excludes_datetime():
    df = pd.DataFrame(columns=["datetime", "AT", "CO", "NOX"])
    assert get_sensor_columns(df) == ["AT", "CO", "NOX"]
