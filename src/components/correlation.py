import pandas as pd
import plotly.graph_objects as go
from dash import dcc

from labels import display_name
from theme import DIVERGING_SCALE, apply_chart_style


def build_correlation_figure(filtered_df: pd.DataFrame) -> go.Figure:
    columns = [c for c in filtered_df.columns if c != "datetime"]
    corr = filtered_df[columns].corr()
    names = [display_name(c) for c in corr.columns]
    fig = go.Figure(
        data=go.Heatmap(
            z=corr.values,
            x=names,
            y=names,
            colorscale=DIVERGING_SCALE,
            zmin=-1,
            zmax=1,
        )
    )
    apply_chart_style(fig)
    # Near-zero cells are transparent (DIVERGING_SCALE), so gridlines would show through them.
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    return fig


def render(filtered_df: pd.DataFrame):
    columns = [c for c in filtered_df.columns if c != "datetime"]
    if len(columns) < 2:
        return "상관관계는 컬럼을 2개 이상 선택해야 표시됩니다."
    return dcc.Graph(figure=build_correlation_figure(filtered_df))
