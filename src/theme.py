import plotly.graph_objects as go

# Chart colors are named by role, not hue. They're mid-tones chosen to stay >= 3:1 contrast
# on both the light (#FFFFFF) and dark (#1C2024) surfaces, since figures are built
# server-side and can't read CSS vars.
SERIES_COLOR = "#5F9A93"  # default data ink (sage teal)
HIGHLIGHT_COLOR = "#EA580C"  # hovered bar / point / crosshair
DIVERGING_NEGATIVE_COLOR = "#0D9488"
DIVERGING_POSITIVE_COLOR = "#EA580C"
FONT_COLOR = "#8a8f89"
GRID_COLOR = "rgba(128,128,128,0.15)"

# Transparent midpoint lets weak correlations fade into whichever theme background is showing.
DIVERGING_SCALE = [
    [0.0, DIVERGING_NEGATIVE_COLOR],
    [0.5, "rgba(138,145,139,0)"],
    [1.0, DIVERGING_POSITIVE_COLOR],
]


def apply_chart_style(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color=FONT_COLOR,
        hoverlabel_bordercolor=HIGHLIGHT_COLOR,
    )
    fig.update_xaxes(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR)
    fig.update_yaxes(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR)
    return fig


def enable_hover_highlight(fig: go.Figure) -> go.Figure:
    """Opt a figure into assets/chart_hover.js: hovered bars turn HIGHLIGHT_COLOR, and line
    charts get a crosshair + value markers across every subplot."""
    fig.update_layout(meta={"hoverHighlight": HIGHLIGHT_COLOR}, hovermode="x")
    return fig
