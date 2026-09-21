from functools import lru_cache
from pathlib import Path

import pandas as pd

CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "raw" / "merged_df.csv"


@lru_cache(maxsize=1)
def load_data() -> pd.DataFrame:
    """merged_df.csv를 로드해 캐싱된 DataFrame으로 반환"""
    return pd.read_csv(CSV_PATH, parse_dates=["datetime"])


def get_years(df: pd.DataFrame) -> list[int]:
    return sorted(df["datetime"].dt.year.unique().tolist())


def get_sensor_columns(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns if c != "datetime"]
