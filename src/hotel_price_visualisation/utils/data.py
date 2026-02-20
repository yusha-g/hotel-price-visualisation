import pandas as pd
from hotel_price_visualisation.config import DATA_FILE
from hotel_price_visualisation.utils.calendar import contruct_calendar


def align_years(df: pd.DataFrame) -> pd.DataFrame:
    cal = contruct_calendar()
    aligned = []

    for year, group in df.groupby("year"):
        merged = cal.merge(group, on=["month", "day"], how="left")
        merged["year"] = year

        reference_date = pd.to_datetime(
            dict(
                year=2000,
                month=merged["month"],
                day=merged["day"],
            )
        )
        merged["md_label"] = reference_date.dt.strftime("%b %d")

        aligned.append(merged)

    result = pd.concat(aligned, ignore_index=True)
    result["day_of_week"] = result["date"].dt.day_name()
    return result


def format_data(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.lower()
    df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y")

    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day

    return align_years(df)


def load_and_prepare_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_FILE)
    return format_data(df)
