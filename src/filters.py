import pandas as pd


def filter_data(df: pd.DataFrame, years: list[int], columns: list[str]) -> pd.DataFrame:
    mask = df["datetime"].dt.year.isin(years)
    return df.loc[mask, ["datetime"] + columns]


def format_summary(filtered_df: pd.DataFrame, years: list[int], columns: list[str]) -> str:
    years_str = ", ".join(str(y) for y in sorted(years))
    return (
        f"선택된 연도: {years_str} / "
        f"컬럼: {len(columns)}개 / "
        f"필터링된 행 수: {len(filtered_df):,}행"
    )
