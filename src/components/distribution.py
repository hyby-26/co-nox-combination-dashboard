import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import dcc
from plotly.subplots import make_subplots

from labels import display_name
from theme import SERIES_COLOR, apply_chart_style, enable_hover_highlight


def build_histogram_figure(filtered_df: pd.DataFrame, bins: int = 50) -> go.Figure:
    columns = [c for c in filtered_df.columns if c != "datetime"]
    fig = make_subplots(
        rows=len(columns), cols=1, subplot_titles=[display_name(c) for c in columns]
    )
    for i, col in enumerate(columns, start=1):
        counts, edges = np.histogram(filtered_df[col], bins=bins)
        centers = (edges[:-1] + edges[1:]) / 2
        fig.add_trace(
            go.Bar(
                x=centers,
                y=counts,
                name=display_name(col),
                marker_color=SERIES_COLOR,
                hovertemplate="%{y:,}건<extra></extra>",
            ),
            row=i,
            col=1,
        )
    fig.update_layout(height=300 * len(columns), showlegend=False)
    fig.update_xaxes(hoverformat=".2f")
    apply_chart_style(fig)
    return enable_hover_highlight(fig)


def render(filtered_df: pd.DataFrame):
    columns = [c for c in filtered_df.columns if c != "datetime"]
    if not columns:
        return "컬럼을 1개 이상 선택하세요."
    return dcc.Graph(figure=build_histogram_figure(filtered_df))
