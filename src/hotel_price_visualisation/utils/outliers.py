import pandas as pd


def _iqr_filter(group: pd.DataFrame, iqr_multiplier: float = 1.5) -> pd.DataFrame:
    q1 = group["price"].quantile(0.25)
    q3 = group["price"].quantile(0.75)
    iqr = q3 - q1

    lower = q1 - iqr_multiplier * iqr
    upper = q3 + iqr_multiplier * iqr

    mask = (group["price"] < lower) | (group["price"] > upper)

    return group[mask]


def detect_outlier_iqr(
    df: pd.DataFrame, iqr_multiplier: float = 1.5, grouping_param: str | None = "year"
) -> pd.DataFrame:
    if grouping_param is None:
        outliers = _iqr_filter(df, iqr_multiplier)
        return outliers

    outliers = [
        _iqr_filter(group, iqr_multiplier) for _, group in df.groupby(grouping_param)
    ]

    if outliers:
        return pd.concat(outliers)
    return pd.DataFrame()
