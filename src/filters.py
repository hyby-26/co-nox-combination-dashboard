import pandas as pd


def filter_data(df: pd.DataFrame, years: list[int], columns: list[str]) -> pd.DataFrame:
    mask = df["datetime"].dt.year.isin(years)
    return df.loc[mask, ["datetime"] + columns]


def format_year_ranges(years: list[int]) -> str:
    sorted_years = sorted(years)
    ranges: list[tuple[int, int]] = []
    start = prev = sorted_years[0]
    for y in sorted_years[1:]:
        if y == prev + 1:
            prev = y
            continue
        ranges.append((start, prev))
        start = prev = y
    ranges.append((start, prev))
    return ", ".join(f"{a}" if a == b else f"{a}–{b}" for a, b in ranges)
