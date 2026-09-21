import pandas as pd

from components.summary_tiles import build_summary_tiles


def _sample_df(n: int) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "datetime": pd.date_range("2011-01-01", periods=n, freq="D"),
            "CO": range(n),
        }
    )


def test_build_summary_tiles_shows_year_range_column_count_and_row_count():
    div = build_summary_tiles(
        _sample_df(3),
        selected_years=[2011, 2012, 2014],
        selected_columns=["CO"],
        all_columns=["CO", "NOX"],
    )
    values = [tile.children[1].children for tile in div.children]
    assert values == ["2011–2012, 2014", "1 / 2개", "3행"]


def test_build_summary_tiles_labels_each_tile():
    div = build_summary_tiles(
        _sample_df(1),
        selected_years=[2011],
        selected_columns=["CO"],
        all_columns=["CO"],
    )
    labels = [tile.children[0].children for tile in div.children]
    assert labels == ["선택 연도", "선택 컬럼", "필터링된 행수"]
