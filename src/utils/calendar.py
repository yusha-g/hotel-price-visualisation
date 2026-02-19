import pandas as pd

REFERENCE_YEAR = 2012  # has 29 days in feb
START_DATE = f"{REFERENCE_YEAR}-01-01"
END_DATE = f"{REFERENCE_YEAR}-12-31"


def contruct_calendar() -> pd.DataFrame:
    calendar = pd.date_range(START_DATE, END_DATE, freq="D")

    all_month_days = pd.DataFrame(
        {"month": calendar.month, "day": calendar.day}
    ).drop_duplicates()

    return all_month_days


def get_period_boundaries(freq: str) -> list[int]:
    periods = pd.date_range(START_DATE, END_DATE, freq=freq)

    return [d.dayofyear for d in periods if d.dayofyear != 1]
