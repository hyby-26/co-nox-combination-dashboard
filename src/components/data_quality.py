import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html

from labels import display_name
from theme import SERIES_COLOR, apply_chart_style, enable_hover_highlight


def build_row_count_figure(filtered_df: pd.DataFrame) -> go.Figure:
    counts = filtered_df["datetime"].dt.year.value_counts().sort_index()
    fig = go.Figure(
        data=go.Bar(
            x=counts.index.astype(str),
            y=counts.values,
            marker_color=SERIES_COLOR,
            hovertemplate="%{y:,}행<extra></extra>",
        )
    )
    apply_chart_style(fig)
    return enable_hover_highlight(fig)


def build_missing_value_table(filtered_df: pd.DataFrame) -> html.Table:
    columns = [c for c in filtered_df.columns if c != "datetime"]
    missing = filtered_df[columns].isna().sum()
    header = html.Tr([html.Th("컬럼"), html.Th("결측치 개수")])
    rows = [html.Tr([html.Td(display_name(col)), html.Td(str(int(count)))]) for col, count in missing.items()]
    return html.Table([header] + rows)


def render(filtered_df: pd.DataFrame) -> html.Div:
    return html.Div(
        [
            dcc.Graph(figure=build_row_count_figure(filtered_df)),
            html.Div(build_missing_value_table(filtered_df), className="table-scroll"),
        ]
    )
