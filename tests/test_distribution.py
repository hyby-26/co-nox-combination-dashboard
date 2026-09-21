import pandas as pd

from components.distribution import build_histogram_figure


def test_build_histogram_figure_creates_one_trace_per_column():
    df = pd.DataFrame({
        "datetime": pd.to_datetime(["2011-01-01", "2011-01-02", "2011-01-03"]),
        "AT": [1.0, 2.0, 3.0],
        "CO": [10.0, 20.0, 30.0],
    })
    fig = build_histogram_figure(df)
    assert len(fig.data) == 2
    assert [trace.name for trace in fig.data] == ["AT", "CO"]


def test_build_histogram_figure_uses_column_values():
    df = pd.DataFrame({
        "datetime": pd.to_datetime(["2011-01-01", "2011-01-02"]),
        "AT": [5.0, 6.0],
    })
    fig = build_histogram_figure(df)
    assert list(fig.data[0].x) == [5.0, 6.0]
