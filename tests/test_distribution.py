import pandas as pd

from components.distribution import build_histogram_figure
from theme import FONT_COLOR, HIGHLIGHT_COLOR, SERIES_COLOR


def test_build_histogram_figure_creates_one_trace_per_column():
    df = pd.DataFrame({
        "datetime": pd.date_range("2011-01-01", periods=100, freq="h"),
        "AT": range(100),
        "CO": range(100),
    })
    fig = build_histogram_figure(df, bins=10)
    assert len(fig.data) == 2
    assert [trace.name for trace in fig.data] == ["AT", "CO"]


def test_build_histogram_figure_bins_server_side_with_requested_bin_count():
    df = pd.DataFrame({
        "datetime": pd.date_range("2011-01-01", periods=100, freq="h"),
        "AT": range(100),
    })
    fig = build_histogram_figure(df, bins=10)
    assert len(fig.data[0].x) == 10
    assert len(fig.data[0].y) == 10


def test_build_histogram_figure_bin_counts_sum_to_row_count():
    df = pd.DataFrame({
        "datetime": pd.date_range("2011-01-01", periods=50, freq="h"),
        "AT": range(50),
    })
    fig = build_histogram_figure(df, bins=5)
    assert sum(fig.data[0].y) == 50


def test_build_histogram_figure_default_bin_count_is_50():
    df = pd.DataFrame({
        "datetime": pd.date_range("2011-01-01", periods=200, freq="h"),
        "AT": range(200),
    })
    fig = build_histogram_figure(df)
    assert len(fig.data[0].x) == 50


def test_build_histogram_figure_uses_single_series_color_and_display_names():
    df = pd.DataFrame({
        "datetime": pd.date_range("2011-01-01", periods=100, freq="h"),
        "AT": range(100),
        "CO": range(100),
        "NOX": range(100),
    })
    fig = build_histogram_figure(df, bins=10)
    assert [trace.marker.color for trace in fig.data] == [SERIES_COLOR] * 3
    assert [a.text for a in fig.layout.annotations] == ["AT", "CO", "NOx"]
    assert fig.data[2].name == "NOx"


def test_build_histogram_figure_opts_into_hover_highlight():
    df = pd.DataFrame({
        "datetime": pd.date_range("2011-01-01", periods=100, freq="h"),
        "AT": range(100),
    })
    fig = build_histogram_figure(df, bins=10)
    assert fig.layout.meta == {"hoverHighlight": HIGHLIGHT_COLOR}


def test_build_histogram_figure_applies_shared_chart_style():
    df = pd.DataFrame({
        "datetime": pd.date_range("2011-01-01", periods=100, freq="h"),
        "AT": range(100),
    })
    fig = build_histogram_figure(df, bins=10)
    assert fig.layout.font.color == FONT_COLOR
    assert fig.layout.paper_bgcolor == "rgba(0,0,0,0)"


def test_build_histogram_figure_formats_hover_without_trace_name_box():
    df = pd.DataFrame({
        "datetime": pd.date_range("2011-01-01", periods=100, freq="h"),
        "AT": range(100),
    })
    fig = build_histogram_figure(df, bins=10)
    assert fig.data[0].hovertemplate == "%{y:,}건<extra></extra>"
    assert fig.layout.xaxis.hoverformat == ".2f"
