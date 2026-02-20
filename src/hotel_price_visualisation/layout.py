import calendar
from dash import html, dcc
import dash_daq as daq
import pandas as pd


def build_primary_options(df: pd.DataFrame) -> html.Div:
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


def build_secondary_options() -> html.Div:
    plot_type_selector = dcc.RadioItems(
        id="plot-type-selector",
        options=[
            {"label": "Line (pattern comparison)", "value": "line"},
            {"label": "Scatter (outlier visualisation)", "value": "scatter"},
        ],
        value="line",
        inline=True,
        style={"flex": "1"},
    )

    comparison_toggle = dcc.RadioItems(
        id="comparison-toggle",
        options=[
            {"label": "Linear Mode", "value": "normal"},
            {"label": "Overlap Mode", "value": "overlap"},
        ],
        value="overlap",
        inline=True,
        style={"flex": "1"},
    )

    multiplier_slider = html.Div(
        [
            daq.ToggleSwitch(
                id="iqr-multiplier-toggle",
                value=True,
                color="purple",
                size=30,
            ),
            dcc.Slider(
                id="iqr-multiplier-slider",
                min=1.5,
                max=4,
                step=0.25,
                value=1.5,
                marks={
                    1.5: "1.5",
                    2: "2",
                    3: "3",
                    4: "4",
                },
            ),
        ],
        style={"flex": "1"},
    )

    return html.Div(
        children=[plot_type_selector, comparison_toggle, multiplier_slider],
        style={
            "display": "flex",
            "gap": "10px",
            "alignItems": "center",
        },
    )


def build_layout(df: pd.DataFrame) -> html.Div:
    graph = dcc.Graph(id="price-graph")
    return html.Div(
        [
            build_primary_options(df),
            build_secondary_options(),
            graph,
        ]
    )
