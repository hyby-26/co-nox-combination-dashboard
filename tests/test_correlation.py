import pandas as pd

from components.correlation import build_correlation_figure
from theme import DIVERGING_NEGATIVE_COLOR, DIVERGING_POSITIVE_COLOR, FONT_COLOR


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


def test_build_correlation_figure_uses_theme_diverging_scale():
    df = pd.DataFrame({
        "datetime": pd.to_datetime(["2011-01-01", "2011-01-02", "2011-01-03"]),
        "AT": [1.0, 2.0, 3.0],
        "CO": [3.0, 2.0, 1.0],
    })
    fig = build_correlation_figure(df)
    scale = fig.data[0].colorscale
    # Plotly normalizes colorscales to tuples; compare stop values only.
    assert (scale[0][0], scale[0][1]) == (0.0, DIVERGING_NEGATIVE_COLOR)
    assert (scale[-1][0], scale[-1][1]) == (1.0, DIVERGING_POSITIVE_COLOR)
    assert fig.layout.font.color == FONT_COLOR


def test_build_correlation_figure_hides_grid_behind_transparent_cells():
    df = pd.DataFrame({
        "datetime": pd.to_datetime(["2011-01-01", "2011-01-02", "2011-01-03"]),
        "AT": [1.0, 2.0, 3.0],
        "CO": [3.0, 2.0, 1.0],
    })
    fig = build_correlation_figure(df)
    assert fig.layout.xaxis.showgrid is False
    assert fig.layout.yaxis.showgrid is False


def test_build_correlation_figure_uses_display_names_on_axes():
    df = pd.DataFrame({
        "datetime": pd.to_datetime(["2011-01-01", "2011-01-02", "2011-01-03"]),
        "AT": [1.0, 2.0, 3.0],
        "NOX": [3.0, 2.0, 1.0],
    })
    fig = build_correlation_figure(df)
    assert list(fig.data[0].x) == ["AT", "NOx"]
    assert list(fig.data[0].y) == ["AT", "NOx"]
