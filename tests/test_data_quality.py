import pandas as pd

from components.data_quality import build_row_count_figure, build_missing_value_table
from theme import FONT_COLOR, HIGHLIGHT_COLOR, SERIES_COLOR


def test_build_row_count_figure_counts_rows_per_year():
    df = pd.DataFrame({
        "datetime": pd.to_datetime(["2011-01-01", "2011-06-01", "2012-01-01"]),
    })
    fig = build_row_count_figure(df)
    assert list(fig.data[0].x) == ["2011", "2012"]
    assert list(fig.data[0].y) == [2, 1]


def test_build_missing_value_table_counts_missing_per_column():
    df = pd.DataFrame({
        "datetime": pd.to_datetime(["2011-01-01", "2011-01-02", "2011-01-03"]),
        "AT": [1.0, None, 3.0],
        "CO": [1.0, 2.0, 3.0],
    })
    table = build_missing_value_table(df)
    at_row_cells = table.children[1].children
    assert at_row_cells[0].children == "AT"
    assert at_row_cells[1].children == "1"
    co_row_cells = table.children[2].children
    assert co_row_cells[1].children == "0"


def test_build_row_count_figure_uses_series_color_with_hover_highlight():
    df = pd.DataFrame({
        "datetime": pd.to_datetime(["2011-01-01", "2012-01-01"]),
    })
    fig = build_row_count_figure(df)
    assert fig.data[0].marker.color == SERIES_COLOR
    assert fig.layout.font.color == FONT_COLOR
    assert fig.layout.meta == {"hoverHighlight": HIGHLIGHT_COLOR}


def test_build_missing_value_table_uses_display_names():
    df = pd.DataFrame({
        "datetime": pd.to_datetime(["2011-01-01"]),
        "NOX": [1.0],
    })
    table = build_missing_value_table(df)
    assert table.children[1].children[0].children == "NOx"


def test_build_row_count_figure_formats_hover_without_trace_name_box():
    df = pd.DataFrame({"datetime": pd.to_datetime(["2011-01-01"])})
    fig = build_row_count_figure(df)
    assert fig.data[0].hovertemplate == "%{y:,}행<extra></extra>"
