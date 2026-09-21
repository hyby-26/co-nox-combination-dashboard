import pandas as pd
import plotly.graph_objects as go
from dash import dcc
from plotly.subplots import make_subplots


def build_timeseries_figure(filtered_df: pd.DataFrame, resample_rule: str = "D") -> go.Figure:
    columns = [c for c in filtered_df.columns if c != "datetime"]
    resampled = (
        filtered_df.set_index("datetime")[columns]
        .resample(resample_rule)
        .mean()
        .dropna(how="all")
        .reset_index()
    )
    fig = make_subplots(rows=len(columns), cols=1, subplot_titles=columns, shared_xaxes=True)
    for i, col in enumerate(columns, start=1):
        fig.add_trace(
            go.Scattergl(x=resampled["datetime"], y=resampled[col], mode="lines", name=col),
            row=i,
            col=1,
        )
    fig.update_layout(
        height=300 * len(columns),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#8a8f89",
    )
    fig.update_xaxes(gridcolor="rgba(128,128,128,0.15)", zerolinecolor="rgba(128,128,128,0.15)")
    fig.update_yaxes(gridcolor="rgba(128,128,128,0.15)", zerolinecolor="rgba(128,128,128,0.15)")
    return fig


def render(filtered_df: pd.DataFrame):
    columns = [c for c in filtered_df.columns if c != "datetime"]
    if not columns:
        return "컬럼을 1개 이상 선택하세요."
    return dcc.Graph(figure=build_timeseries_figure(filtered_df))
