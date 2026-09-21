import pandas as pd
import plotly.graph_objects as go

from components.timeseries import build_timeseries_figure


def test_build_timeseries_figure_creates_one_trace_per_column():
    df = pd.DataFrame({
        "datetime": pd.to_datetime(["2011-01-01", "2011-01-02", "2011-01-03"]),
        "AT": [1.0, 2.0, 3.0],
        "CO": [10.0, 20.0, 30.0],
    })
    fig = build_timeseries_figure(df)
    assert len(fig.data) == 2
    assert [trace.name for trace in fig.data] == ["AT", "CO"]


def test_build_timeseries_figure_uses_scattergl_for_performance():
    df = pd.DataFrame({
        "datetime": pd.to_datetime(["2011-01-01", "2011-01-02"]),
        "AT": [1.0, 2.0],
    })
    fig = build_timeseries_figure(df)
    assert isinstance(fig.data[0], go.Scattergl)


def test_build_timeseries_figure_uses_datetime_as_x_axis():
    df = pd.DataFrame({
        "datetime": pd.to_datetime(["2011-01-01", "2011-01-02"]),
        "AT": [5.0, 6.0],
    })
    fig = build_timeseries_figure(df)
    assert list(fig.data[0].x) == list(pd.to_datetime(["2011-01-01", "2011-01-02"]))
    assert list(fig.data[0].y) == [5.0, 6.0]
