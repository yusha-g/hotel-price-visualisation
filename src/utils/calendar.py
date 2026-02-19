import pandas as pd

REFERENCE_YEAR = 2012  # has 29 days in feb


def contruct_calendar_for_legend() -> pd.DataFrame:
    calendar = pd.date_range(
        f"{REFERENCE_YEAR}-01-01", f"{REFERENCE_YEAR}-12-31", freq="D"
    )

    all_month_days = pd.DataFrame(
        {"month": calendar.month, "day": calendar.day}
    ).drop_duplicates()

    return all_month_days


def get_period_boundaries(freq: str) -> list[int]:
    reference_year = 2012
    start = pd.Timestamp(f"{reference_year}-01-01")
    end = pd.Timestamp(f"{reference_year}-12-31")

    periods = pd.date_range(start=start, end=end, freq=freq)

    return [d.dayofyear for d in periods if d.dayofyear != 1]
