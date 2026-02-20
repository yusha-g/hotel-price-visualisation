import pandas as pd


def detect_outlier_iqr(
    df: pd.DataFrame, iqr_multiplier: float = 1.5, grouping_param: str = "year"
) -> pd.DataFrame:
    outliers = []

    for _, group in df.groupby(grouping_param):
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
