from dash import Input, Output, callback
import plotly.graph_objects as go
import plotly.express as px
from utils.calendar import get_period_boundaries
from utils.data import load_and_prepare_data


df = load_and_prepare_data()


@callback(  # type: ignore[misc]
    Output("dropdown-period-selector", "disabled"),
    Input("month-filter", "value"),
)
def toggle_period_selector(selected_month: list[int] | None) -> bool:
    if selected_month:
        return True
    return False


@callback(  # type: ignore[misc]
    Output("month-filter", "disabled"),
    Input("dropdown-period-selector", "value"),
)
def toggle_month_selector(period_selector: list[int] | None) -> bool:
    if period_selector:
        return True
    return False


@callback(  # type: ignore[misc]
    Output("price-graph", "figure"),
    Input("price-graph", "figure"),
    Input("dropdown-year", "value"),
    Input("dropdown-period-selector", "value"),
    Input("month-filter", "value"),
)
def update_graph(
    fig: go.Figure,
    selected_years: list[int],
    period: str,
    selected_months: list[int],
) -> go.Figure:
    filtered_df = df[df["year"].isin(selected_years)]
    if selected_months:
        filtered_df = filtered_df[filtered_df["month"].isin(selected_months)]
    boundaries = []
    if period:
        boundaries = get_period_boundaries(period)
    fig = px.line(
        filtered_df,
        x="md_label",
        y="price",
        color="year",
        custom_data=["date"],
        color_discrete_sequence=px.colors.qualitative.Dark24,
        labels={"md_label": "Date", "price": "Price", "year": "Year"},
        title="Price Trend by Year",
    )

    for boundary in boundaries:
        fig.add_vline(
            x=boundary,
            line_width=1,
            line_dash="dot",
            line_color="blue",
            opacity=0.6,
        )
    fig.update_layout(template="plotly_white", hovermode="x unified")
    fig.update_traces(
        hovertemplate="<b>Date:</b> %{customdata[0]|%m-%d}<br>"
        + "<b>Price:</b> %{y}<br>"
    )
    return fig
