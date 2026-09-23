import pandas as pd
from dash import html

from labels import display_name


def build_metadata_summary(full_start: pd.Timestamp, full_end: pd.Timestamp) -> html.Div:
    return html.Div([html.P(f"데이터 전체 기간: {full_start:%Y-%m-%d} ~ {full_end:%Y-%m-%d}")])


def build_summary_stats_table(filtered_df: pd.DataFrame) -> html.Table:
    columns = [c for c in filtered_df.columns if c != "datetime"]
    stats = filtered_df[columns].describe()
    header = html.Tr([html.Th("통계")] + [html.Th(display_name(col)) for col in columns])
    rows = [
        html.Tr(
            [html.Td(stat_name)]
            + [html.Td(f"{stats.loc[stat_name, col]:.3f}") for col in columns]
        )
        for stat_name in stats.index
    ]
    return html.Table([header] + rows)


def render(filtered_df: pd.DataFrame, full_start: pd.Timestamp, full_end: pd.Timestamp) -> html.Div:
    columns = [c for c in filtered_df.columns if c != "datetime"]
    if not columns:
        return "컬럼을 1개 이상 선택하세요."
    return html.Div(
        [
            build_metadata_summary(full_start, full_end),
            html.Div(build_summary_stats_table(filtered_df), className="table-scroll"),
        ]
    )
