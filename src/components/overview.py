import pandas as pd
from dash import html


def build_metadata_summary(filtered_df: pd.DataFrame) -> html.Div:
    start = filtered_df["datetime"].min()
    end = filtered_df["datetime"].max()
    return html.Div([html.P(f"기간: {start:%Y-%m-%d} ~ {end:%Y-%m-%d}")])


def build_summary_stats_table(filtered_df: pd.DataFrame) -> html.Table:
    columns = [c for c in filtered_df.columns if c != "datetime"]
    stats = filtered_df[columns].describe()
    header = html.Tr([html.Th("통계")] + [html.Th(col) for col in columns])
    rows = [
        html.Tr(
            [html.Td(stat_name)]
            + [html.Td(f"{stats.loc[stat_name, col]:.3f}") for col in columns]
        )
        for stat_name in stats.index
    ]
    return html.Table([header] + rows)


def render(filtered_df: pd.DataFrame) -> html.Div:
    columns = [c for c in filtered_df.columns if c != "datetime"]
    if not columns:
        return "컬럼을 1개 이상 선택하세요."
    return html.Div(
        [
            build_metadata_summary(filtered_df),
            html.Div(build_summary_stats_table(filtered_df), className="table-scroll"),
        ]
    )
