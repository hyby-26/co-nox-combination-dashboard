import pandas as pd

from filters import filter_data, format_summary


def _sample_df():
    return pd.DataFrame({
        "datetime": pd.to_datetime(["2011-01-01", "2012-01-01", "2013-01-01"]),
        "AT": [1, 2, 3],
        "CO": [10, 20, 30],
        "NOX": [100, 200, 300],
    })


def test_filter_data_filters_rows_by_year():
    result = filter_data(_sample_df(), years=[2011, 2013], columns=["CO"])
    assert result["CO"].tolist() == [10, 30]


def test_filter_data_keeps_only_selected_columns_plus_datetime():
    result = filter_data(_sample_df(), years=[2011, 2012, 2013], columns=["CO"])
    assert list(result.columns) == ["datetime", "CO"]


def test_format_summary_includes_years_column_count_and_row_count():
    filtered = pd.DataFrame({
        "datetime": pd.to_datetime(["2011-01-01", "2011-01-02"]),
        "CO": [1, 2],
    })
    summary = format_summary(filtered, years=[2011], columns=["CO"])
    assert "2011" in summary
    assert "1개" in summary
    assert "2행" in summary
