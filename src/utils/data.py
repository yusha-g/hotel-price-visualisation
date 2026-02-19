import pandas as pd
from config import DATA_FILE
from utils.calendar import contruct_calendar_for_legend


def get_data() -> pd.DataFrame:
    return pd.read_csv(DATA_FILE)


def align_years(df: pd.DataFrame) -> pd.DataFrame:
    cal = contruct_calendar_for_legend()
    aligned = []
    for year, group in df.groupby("year"):
        merged = cal.merge(group, on=["month", "day"], how="left")
        merged["year"] = year
        merged["seasonal_date"] = pd.to_datetime(
            dict(
                year=2000,
                month=merged["month"],
                day=merged["day"],
            )
        )
        merged["md_label"] = merged["seasonal_date"].dt.strftime("%b %d")
        aligned.append(merged)
    aligned_df = pd.concat(aligned, ignore_index=True).drop(
        ["seasonal_date", "day"], axis=1
    )
    return aligned_df


def format_data(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.lower()
    df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y")
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day
    aligned_df = align_years(df)
    return aligned_df


def load_and_prepare_data() -> pd.DataFrame:
    df = get_data()
    return format_data(df)
