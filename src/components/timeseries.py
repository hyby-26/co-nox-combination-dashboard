import pandas as pd
import plotly.graph_objects as go
from dash import dcc
from plotly.subplots import make_subplots


def build_timeseries_figure(filtered_df: pd.DataFrame) -> go.Figure:
    columns = [c for c in filtered_df.columns if c != "datetime"]
    fig = make_subplots(rows=len(columns), cols=1, subplot_titles=columns, shared_xaxes=True)
    for i, col in enumerate(columns, start=1):
        fig.add_trace(
            go.Scattergl(x=filtered_df["datetime"], y=filtered_df[col], mode="lines", name=col),
            row=i,
            col=1,
        )
    fig.update_layout(height=300 * len(columns), showlegend=False)
    return fig


def render(filtered_df: pd.DataFrame):
    columns = [c for c in filtered_df.columns if c != "datetime"]
    if not columns:
        return "컬럼을 1개 이상 선택하세요."
    return dcc.Graph(figure=build_timeseries_figure(filtered_df))
