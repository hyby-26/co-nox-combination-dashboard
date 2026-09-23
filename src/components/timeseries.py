import pandas as pd
import plotly.graph_objects as go
from dash import dcc
from plotly.subplots import make_subplots

from labels import display_name
from theme import SERIES_COLOR, apply_chart_style, enable_hover_highlight

# Line traces autorange to exactly [min, max], so series pinned near their max (e.g. TAT
# at ~550) hug the plot edge and look clipped. Pad each subplot by this share of its span.
Y_RANGE_PADDING = 0.10


def _padded_range(values: pd.Series) -> list[float] | None:
    low, high = values.min(), values.max()
    if pd.isna(low):
        return None
    pad = (high - low) * Y_RANGE_PADDING or max(abs(high) * Y_RANGE_PADDING, 1.0)
    return [low - pad, high + pad]


def _share_one_x_axis(fig: go.Figure, rows: int) -> None:
    """Move every row onto the single `x` axis. make_subplots gives each row its own x axis
    (x, x2, ...) matched together, but hoversubplots="axis" only gathers subplots that share
    the same axis object — so the unified hover label would otherwise list just one row.
    Call it last: update_xaxes() walks make_subplots' grid and would recreate x2, x3, ..."""
    fig.update_traces(xaxis="x")
    for i in range(2, rows + 1):
        fig.layout[f"xaxis{i}"] = None
        fig.layout[f"yaxis{i}"].anchor = "x"
    # Date ticks belong under the bottom row, where make_subplots had put them.
    fig.layout.xaxis.update(
        matches=None, anchor="y" if rows == 1 else f"y{rows}", showticklabels=True
    )


def build_timeseries_figure(filtered_df: pd.DataFrame, resample_rule: str = "D") -> go.Figure:
    columns = [c for c in filtered_df.columns if c != "datetime"]
    resampled = (
        filtered_df.set_index("datetime")[columns]
        .resample(resample_rule)
        .mean()
        .dropna(how="all")
        .reset_index()
    )
    fig = make_subplots(
        rows=len(columns),
        cols=1,
        subplot_titles=[display_name(c) for c in columns],
        shared_xaxes=True,
    )
    for i, col in enumerate(columns, start=1):
        fig.add_trace(
            go.Scattergl(
                x=resampled["datetime"],
                y=resampled[col],
                mode="lines",
                name=display_name(col),
                line_color=SERIES_COLOR,
                hovertemplate=f"<b>{display_name(col)}</b> %{{y:.2f}}<extra></extra>",
            ),
            row=i,
            col=1,
        )
        y_range = _padded_range(resampled[col])
        if y_range is not None:
            fig.update_yaxes(range=y_range, row=i, col=1)
    fig.update_layout(height=300 * len(columns), showlegend=False)
    # chart_hover.js draws the crosshair, so Plotly's unified-hover spike line is off.
    fig.update_xaxes(
        hoverformat="%Y-%m-%d",
        showspikes=False,
        unifiedhovertitle_text="<b>%{x|%Y-%m-%d}</b>",
    )
    apply_chart_style(fig)
    enable_hover_highlight(fig)
    # One label listing every column at the hovered date, since the rows don't fit on one screen.
    fig.update_layout(hovermode="x unified", hoversubplots="axis")
    _share_one_x_axis(fig, len(columns))
    return fig


def render(filtered_df: pd.DataFrame):
    columns = [c for c in filtered_df.columns if c != "datetime"]
    if not columns:
        return "컬럼을 1개 이상 선택하세요."
    return dcc.Graph(figure=build_timeseries_figure(filtered_df))
