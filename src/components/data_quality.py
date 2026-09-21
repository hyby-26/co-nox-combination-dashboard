import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html


def build_row_count_figure(filtered_df: pd.DataFrame) -> go.Figure:
    counts = filtered_df["datetime"].dt.year.value_counts().sort_index()
    return go.Figure(data=go.Bar(x=counts.index.astype(str), y=counts.values))


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
            build_missing_value_table(filtered_df),
        ]
    )
