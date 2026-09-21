import pandas as pd

from filters import filter_data, format_year_ranges


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


def test_format_year_ranges_collapses_consecutive_years():
    assert format_year_ranges([2011, 2012, 2013]) == "2011–2013"


def test_format_year_ranges_splits_non_consecutive_gaps():
    assert format_year_ranges([2011, 2012, 2014, 2015]) == "2011–2012, 2014–2015"


def test_format_year_ranges_handles_single_year():
    assert format_year_ranges([2013]) == "2013"


def test_format_year_ranges_sorts_unordered_input():
    assert format_year_ranges([2015, 2011, 2012]) == "2011–2012, 2015"
