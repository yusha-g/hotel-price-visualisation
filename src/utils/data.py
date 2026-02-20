import pandas as pd
from config import DATA_FILE
from utils.calendar import contruct_calendar


def detect_outlier_iqr(df: pd.DataFrame, iqr_multiplier: float = 1.5) -> pd.DataFrame:
    outliers = []

    for _, group in df.groupby("year"):
        q1 = group["price"].quantile(0.25)
        q3 = group["price"].quantile(0.75)
        iqr = q3 - q1

        lower = q1 - iqr_multiplier * iqr
        upper = q3 + iqr_multiplier * iqr

        mask = (group["price"] < lower) | (group["price"] > upper)

        outliers.append(group[mask])

    if outliers:
        return pd.concat(outliers)
    return pd.DataFrame()


def align_years(df: pd.DataFrame) -> pd.DataFrame:
    cal = contruct_calendar()
    aligned = []
    for year, group in df.groupby("year"):
        merged = cal.merge(group, on=["month", "day"], how="left")
        merged["year"] = year
        merged["reference_date"] = pd.to_datetime(
            dict(
                year=2000,
                month=merged["month"],
                day=merged["day"],
            )
        )
        merged["md_label"] = merged["reference_date"].dt.strftime("%b %d")
        aligned.append(merged)
    aligned_df = pd.concat(aligned, ignore_index=True).drop(
        [
            "reference_date",
        ],
        axis=1,
    )
    aligned_df["day_of_week"] = aligned_df["date"].dt.day_name()
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
    df = pd.read_csv(DATA_FILE)
    return format_data(df)
