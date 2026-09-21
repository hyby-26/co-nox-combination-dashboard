import pandas as pd

from components.overview import build_metadata_summary, build_summary_stats_table


def _sample_df():
    return pd.DataFrame({
        "datetime": pd.to_datetime(["2011-01-01", "2011-01-02", "2011-01-03"]),
        "AT": [1.0, 2.0, 3.0],
        "CO": [10.0, 20.0, 30.0],
    })


def test_build_metadata_summary_reports_row_count_and_date_range():
    div = build_metadata_summary(_sample_df())
    texts = [p.children for p in div.children]
    assert any("3행" in t for t in texts)
    assert any("2011-01-01" in t and "2011-01-03" in t for t in texts)
    assert any("2개" in t for t in texts)


def test_build_summary_stats_table_includes_mean_row_for_each_column():
    table = build_summary_stats_table(_sample_df())
    header_cells = table.children[0].children
    assert [cell.children for cell in header_cells] == ["통계", "AT", "CO"]
    mean_row = next(row for row in table.children[1:] if row.children[0].children == "mean")
    assert mean_row.children[1].children == "2.000"
    assert mean_row.children[2].children == "20.000"
