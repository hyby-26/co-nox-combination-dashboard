import pandas as pd

from components.correlation import build_correlation_figure


def test_build_correlation_figure_uses_correct_axis_labels():
    df = pd.DataFrame({
        "datetime": pd.to_datetime(["2011-01-01", "2011-01-02", "2011-01-03"]),
        "AT": [1.0, 2.0, 3.0],
        "CO": [3.0, 2.0, 1.0],
    })
    fig = build_correlation_figure(df)
    assert list(fig.data[0].x) == ["AT", "CO"]
    assert list(fig.data[0].y) == ["AT", "CO"]


def test_build_correlation_figure_computes_perfect_negative_correlation():
    df = pd.DataFrame({
        "datetime": pd.to_datetime(["2011-01-01", "2011-01-02", "2011-01-03"]),
        "AT": [1.0, 2.0, 3.0],
        "CO": [3.0, 2.0, 1.0],
    })
    fig = build_correlation_figure(df)
    z = fig.data[0].z
    assert round(z[0][1], 5) == -1.0
