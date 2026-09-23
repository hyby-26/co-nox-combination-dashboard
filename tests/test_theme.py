import plotly.graph_objects as go
from plotly.subplots import make_subplots

from theme import (
    DIVERGING_NEGATIVE_COLOR,
    DIVERGING_POSITIVE_COLOR,
    DIVERGING_SCALE,
    FONT_COLOR,
    GRID_COLOR,
    HIGHLIGHT_COLOR,
    SERIES_COLOR,
    apply_chart_style,
    enable_hover_highlight,
)


def test_series_and_highlight_colors_are_sage_teal_and_orange():
    assert SERIES_COLOR == "#5F9A93"
    assert HIGHLIGHT_COLOR == "#EA580C"


def test_diverging_scale_runs_negative_to_transparent_to_positive():
    assert DIVERGING_SCALE[0] == [0.0, DIVERGING_NEGATIVE_COLOR]
    assert DIVERGING_SCALE[1] == [0.5, "rgba(138,145,139,0)"]
    assert DIVERGING_SCALE[2] == [1.0, DIVERGING_POSITIVE_COLOR]


def test_apply_chart_style_sets_transparent_background_and_font():
    fig = apply_chart_style(go.Figure())
    assert fig.layout.paper_bgcolor == "rgba(0,0,0,0)"
    assert fig.layout.plot_bgcolor == "rgba(0,0,0,0)"
    assert fig.layout.font.color == FONT_COLOR


def test_apply_chart_style_outlines_hover_labels_in_highlight_color():
    fig = apply_chart_style(go.Figure())
    assert fig.layout.hoverlabel.bordercolor == HIGHLIGHT_COLOR


def test_apply_chart_style_sets_grid_color_on_every_subplot_axis():
    fig = make_subplots(rows=2, cols=1)
    apply_chart_style(fig)
    for axis in [fig.layout.xaxis, fig.layout.xaxis2, fig.layout.yaxis, fig.layout.yaxis2]:
        assert axis.gridcolor == GRID_COLOR
        assert axis.zerolinecolor == GRID_COLOR


def test_apply_chart_style_returns_same_figure():
    fig = go.Figure()
    assert apply_chart_style(fig) is fig


def test_enable_hover_highlight_marks_figure_for_client_script():
    fig = enable_hover_highlight(go.Figure())
    assert fig.layout.meta == {"hoverHighlight": HIGHLIGHT_COLOR}
    assert fig.layout.hovermode == "x"


def test_apply_chart_style_keeps_side_margins_tight():
    # Plotly's default 80px side margins leave the right side visibly wider than the left
    # (whose margin holds the y tick labels); tick labels still get room via automargin.
    fig = apply_chart_style(go.Figure())
    assert fig.layout.margin.l == fig.layout.margin.r
    assert fig.layout.margin.r <= 16


def test_apply_chart_style_trims_top_margin_but_leaves_room_for_titles():
    # Default 100px leaves an empty band above every chart; subplot titles and the
    # modebar still need a little room up there.
    fig = apply_chart_style(go.Figure())
    assert 24 <= fig.layout.margin.t <= 48
