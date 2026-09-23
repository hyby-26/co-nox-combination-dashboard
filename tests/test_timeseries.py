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
    assert fig.data[0].hovertemplate == "NOx %{y:.2f}<extra></extra>"
    assert fig.layout.xaxis.hoverformat == "%Y-%m-%d"
