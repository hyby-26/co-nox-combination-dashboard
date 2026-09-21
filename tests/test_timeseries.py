import pandas as pd
import plotly.graph_objects as go

from components.timeseries import build_timeseries_figure


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
