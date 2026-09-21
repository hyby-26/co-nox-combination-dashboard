import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import dcc
from plotly.subplots import make_subplots


def build_histogram_figure(filtered_df: pd.DataFrame, bins: int = 50) -> go.Figure:
    columns = [c for c in filtered_df.columns if c != "datetime"]
    fig = make_subplots(rows=len(columns), cols=1, subplot_titles=columns)
    for i, col in enumerate(columns, start=1):
        counts, edges = np.histogram(filtered_df[col], bins=bins)
        centers = (edges[:-1] + edges[1:]) / 2
        fig.add_trace(go.Bar(x=centers, y=counts, name=col), row=i, col=1)
    fig.update_layout(height=300 * len(columns), showlegend=False)
    return fig


def render(filtered_df: pd.DataFrame):
    columns = [c for c in filtered_df.columns if c != "datetime"]
    if not columns:
        return "컬럼을 1개 이상 선택하세요."
    return dcc.Graph(figure=build_histogram_figure(filtered_df))
