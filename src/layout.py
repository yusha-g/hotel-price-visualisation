import calendar
from dash import html, dcc
import pandas as pd


def primary_selection(df: pd.DataFrame) -> html.Div:
    year_dropdown = dcc.Dropdown(
        id="dropdown-year",
        options=[
            {"label": str(year), "value": year} for year in sorted(df["year"].unique())
        ],
        multi=True,
        value=[df["year"].min()],
        placeholder="Select year(s)",
        style={"flex": "1"},
    )
    month_dropdown = dcc.Dropdown(
        id="month-filter",
        options=[{"label": calendar.month_name[m], "value": m} for m in range(1, 13)],
        multi=True,
        style={"flex": "1"},
        placeholder="Select month(s)",
    )
    period_selector = dcc.Dropdown(
        id="dropdown-period-selector",
        options=[
            {"label": "Quarterly", "value": "QS"},
            {"label": "Monthly", "value": "MS"},
            {"label": "Bi-Monthly", "value": "2MS"},
            {"label": "Semi-Annual", "value": "6MS"},
        ],
        clearable=True,
        style={"flex": "1"},
        placeholder="Select period",
    )
    return html.Div(
        id="dropdown-window",
        children=[year_dropdown, month_dropdown, period_selector],
        style={
            "display": "flex",
            "gap": "10px",
            "alignItems": "center",
        },
    )


def contruct_app_layout(df: pd.DataFrame) -> html.Div:
    heading = html.H2("Price Trend Comparison by Year")
    plot_type_selector = dcc.RadioItems(
        id="plot-type-selector",
        options=[
            {"label": "Line", "value": "line"},
            {"label": "Scatter", "value": "scatter"},
        ],
        value="line",
        inline=True,
        style={"flex": "1"},
    )
    graph = dcc.Graph(id="price-graph")
    return html.Div(
        [
            heading,
            primary_selection(df),
            plot_type_selector,
            graph,
        ]
    )
