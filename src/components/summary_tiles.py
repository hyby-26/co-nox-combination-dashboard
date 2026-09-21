import pandas as pd
from dash import html

from filters import format_year_ranges


def _tile(label: str, value: str) -> html.Div:
    return html.Div(
        [
            html.Div(label, className="stat-label"),
            html.Div(value, className="stat-value"),
        ],
        className="stat-tile",
    )


def build_summary_tiles(
    filtered_df: pd.DataFrame,
    selected_years: list[int],
    selected_columns: list[str],
    all_columns: list[str],
) -> html.Div:
    return html.Div(
        [
            _tile("선택 연도", format_year_ranges(selected_years)),
            _tile("선택 컬럼", f"{len(selected_columns)} / {len(all_columns)}개"),
            _tile("필터링된 행수", f"{len(filtered_df):,}행"),
        ],
        className="stat-tiles",
    )
