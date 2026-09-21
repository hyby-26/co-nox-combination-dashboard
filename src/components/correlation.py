import pandas as pd
import plotly.graph_objects as go
from dash import dcc


def build_correlation_figure(filtered_df: pd.DataFrame) -> go.Figure:
    columns = [c for c in filtered_df.columns if c != "datetime"]
    corr = filtered_df[columns].corr()
    return go.Figure(
        data=go.Heatmap(
            z=corr.values,
            x=corr.columns.tolist(),
            y=corr.columns.tolist(),
            colorscale="RdBu",
            zmin=-1,
            zmax=1,
        )
    )


def render(filtered_df: pd.DataFrame):
    columns = [c for c in filtered_df.columns if c != "datetime"]
    if len(columns) < 2:
        return "상관관계는 컬럼을 2개 이상 선택해야 표시됩니다."
    return dcc.Graph(figure=build_correlation_figure(filtered_df))
