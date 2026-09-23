import pandas as pd
import plotly.graph_objects as go

from components.timeseries import build_timeseries_figure
from theme import FONT_COLOR, HIGHLIGHT_COLOR, SERIES_COLOR


def test_build_timeseries_figure_creates_one_trace_per_column():
    df = pd.DataFrame({
        "datetime": pd.date_range("2011-01-01", periods=48, freq="h"),
        "AT": range(48),
        "CO": range(48),
    })
    fig = build_timeseries_figure(df, resample_rule="D")
    assert len(fig.data) == 2
    assert [trace.name for trace in fig.data] == ["AT", "CO"]


def test_build_timeseries_figure_uses_scattergl_for_performance():
    df = pd.DataFrame({
        "datetime": pd.date_range("2011-01-01", periods=48, freq="h"),
        "AT": range(48),
    })
    fig = build_timeseries_figure(df, resample_rule="D")
    assert isinstance(fig.data[0], go.Scattergl)


def test_build_timeseries_figure_resamples_to_requested_rule():
    df = pd.DataFrame({
        "datetime": pd.date_range("2011-01-01", periods=48, freq="h"),
        "AT": [0] * 24 + [10] * 24,
    })
    fig = build_timeseries_figure(df, resample_rule="D")
    assert list(fig.data[0].y) == [0.0, 10.0]
    assert len(fig.data[0].x) == 2


def test_build_timeseries_figure_default_resample_rule_is_daily():
    df = pd.DataFrame({
        "datetime": pd.date_range("2011-01-01", periods=48, freq="h"),
        "AT": range(48),
    })
    fig = build_timeseries_figure(df)
    assert len(fig.data[0].x) == 2


def test_build_timeseries_figure_uses_single_series_color_and_display_names():
    df = pd.DataFrame({
        "datetime": pd.date_range("2011-01-01", periods=48, freq="h"),
        "AT": range(48),
        "CO": range(48),
        "NOX": range(48),
    })
    fig = build_timeseries_figure(df, resample_rule="D")
    assert [trace.line.color for trace in fig.data] == [SERIES_COLOR] * 3
    assert [a.text for a in fig.layout.annotations] == ["AT", "CO", "NOx"]
    assert fig.data[2].name == "NOx"


def test_build_timeseries_figure_opts_into_hover_highlight():
    df = pd.DataFrame({
        "datetime": pd.date_range("2011-01-01", periods=48, freq="h"),
        "AT": range(48),
    })
    fig = build_timeseries_figure(df, resample_rule="D")
    assert fig.layout.meta == {"hoverHighlight": HIGHLIGHT_COLOR}


def test_build_timeseries_figure_applies_shared_chart_style():
    df = pd.DataFrame({
        "datetime": pd.date_range("2011-01-01", periods=48, freq="h"),
        "AT": range(48),
    })
    fig = build_timeseries_figure(df, resample_rule="D")
    assert fig.layout.font.color == FONT_COLOR
    assert fig.layout.paper_bgcolor == "rgba(0,0,0,0)"


def test_build_timeseries_figure_formats_hover_without_trace_name_box():
    df = pd.DataFrame({
        "datetime": pd.date_range("2011-01-01", periods=48, freq="h"),
        "NOX": range(48),
    })
    fig = build_timeseries_figure(df, resample_rule="D")
    assert fig.data[0].hovertemplate == "<b>NOx</b> %{y:.2f}<extra></extra>"
    assert fig.layout.xaxis.hoverformat == "%Y-%m-%d"


def test_build_timeseries_figure_pads_y_range_so_lines_do_not_touch_edges():
    df = pd.DataFrame({
        "datetime": pd.date_range("2011-01-01", periods=48, freq="h"),
        "TAT": [530] * 24 + [550] * 24,
        "CO": [0] * 24 + [10] * 24,
    })
    fig = build_timeseries_figure(df, resample_rule="D")
    assert list(fig.layout.yaxis.range) == [528.0, 552.0]
    assert list(fig.layout.yaxis2.range) == [-1.0, 11.0]


def test_build_timeseries_figure_pads_flat_series():
    df = pd.DataFrame({
        "datetime": pd.date_range("2011-01-01", periods=48, freq="h"),
        "AT": [20] * 48,
    })
    fig = build_timeseries_figure(df, resample_rule="D")
    low, high = fig.layout.yaxis.range
    assert low < 20 < high


def _three_column_df():
    return pd.DataFrame({
        "datetime": pd.date_range("2011-01-01", periods=48, freq="h"),
        "AT": range(48),
        "CO": range(48),
        "NOX": range(48),
    })


def test_build_timeseries_figure_shows_all_columns_in_one_hover_label():
    fig = build_timeseries_figure(_three_column_df(), resample_rule="D")
    assert fig.layout.hovermode == "x unified"
    assert fig.layout.hoversubplots == "axis"


def test_build_timeseries_figure_puts_every_trace_on_one_shared_x_axis():
    # hoversubplots="axis" only gathers subplots that share the same x axis object;
    # make_subplots' per-row matched axes (x, x2, ...) don't count.
    fig = build_timeseries_figure(_three_column_df(), resample_rule="D")
    assert [t.xaxis for t in fig.data] == ["x", "x", "x"]
    assert [t.yaxis for t in fig.data] == ["y", "y2", "y3"]
    layout = fig.to_dict()["layout"]
    assert not [k for k in layout if k.startswith("xaxis") and k != "xaxis"]


def test_build_timeseries_figure_keeps_date_ticks_under_bottom_subplot():
    fig = build_timeseries_figure(_three_column_df(), resample_rule="D")
    assert fig.layout.xaxis.anchor == "y3"
    assert fig.layout.xaxis.showticklabels is not False
    assert [fig.layout[f"yaxis{i}"].anchor for i in ("", 2, 3)] == ["x", "x", "x"]


def test_build_timeseries_figure_leaves_crosshair_to_hover_highlight():
    # chart_hover.js draws the crosshair; Plotly's unified-hover spike would double it.
    fig = build_timeseries_figure(_three_column_df(), resample_rule="D")
    assert fig.layout.xaxis.showspikes is False


def test_build_timeseries_figure_bolds_the_unified_hover_date():
    fig = build_timeseries_figure(_three_column_df(), resample_rule="D")
    assert fig.layout.xaxis.unifiedhovertitle.text == "<b>%{x|%Y-%m-%d}</b>"
