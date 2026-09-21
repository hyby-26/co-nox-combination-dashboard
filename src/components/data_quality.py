import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html


def build_row_count_figure(filtered_df: pd.DataFrame) -> go.Figure:
    counts = filtered_df["datetime"].dt.year.value_counts().sort_index()
    fig = go.Figure(data=go.Bar(x=counts.index.astype(str), y=counts.values))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#8a8f89",
    )
    fig.update_xaxes(gridcolor="rgba(128,128,128,0.15)", zerolinecolor="rgba(128,128,128,0.15)")
    fig.update_yaxes(gridcolor="rgba(128,128,128,0.15)", zerolinecolor="rgba(128,128,128,0.15)")
    return fig


def build_missing_value_table(filtered_df: pd.DataFrame) -> html.Table:
    columns = [c for c in filtered_df.columns if c != "datetime"]
    missing = filtered_df[columns].isna().sum()
    header = html.Tr([html.Th("컬럼"), html.Th("결측치 개수")])
    rows = [html.Tr([html.Td(col), html.Td(str(int(count)))]) for col, count in missing.items()]
    return html.Table([header] + rows)


def render(filtered_df: pd.DataFrame) -> html.Div:
    return html.Div(
        [
            dcc.Graph(figure=build_row_count_figure(filtered_df)),
            html.Div(build_missing_value_table(filtered_df), className="table-scroll"),
        ]
    )
