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
        options=[
            {"label": "January", "value": 1},
            {"label": "February", "value": 2},
            {"label": "March", "value": 3},
            {"label": "April", "value": 4},
            {"label": "May", "value": 5},
            {"label": "June", "value": 6},
            {"label": "July", "value": 7},
            {"label": "August", "value": 8},
            {"label": "September", "value": 9},
            {"label": "October", "value": 10},
            {"label": "November", "value": 11},
            {"label": "December", "value": 12},
        ],
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
    # comparison_toggle = daq.ToggleSwitch(
    #     id="comparison-toggle",
    #     value=True,
    #     color="#2E86C1",
    #     label="Comparison Mode",
    #     labelPosition="bottom"
    # )
    graph = dcc.Graph(id="price-graph")
    return html.Div(
        [
            heading,
            primary_selection(df),
            graph,
        ]
    )
