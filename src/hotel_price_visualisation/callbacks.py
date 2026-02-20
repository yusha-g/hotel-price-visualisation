from typing import Any
from dash import Input, Output, State, callback
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils.calendar import get_period_boundaries
from utils.data import detect_outlier_iqr


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
    Output("iqr-multiplier-slider", "disabled"), Input("iqr-multiplier-toggle", "value")
)
def toggle_iqr_slider(enable_slider: bool) -> bool:
    if enable_slider:
        return False
    return True


@callback(  # type: ignore[misc]
    Output("price-graph", "figure"),
    State("data-store", "data"),
    Input("dropdown-year", "value"),
    Input("dropdown-period-selector", "value"),
    Input("month-filter", "value"),
    Input("plot-type-selector", "value"),
    Input("comparison-toggle", "value"),
    Input("iqr-multiplier-slider", "value"),
    Input("iqr-multiplier-slider", "disabled"),
)
def update_graph(
    data: dict[str, Any],
    selected_years: list[int],
    period: str,
    selected_months: list[int],
    plot_type: str,
    comparison_mode: str,
    iqr_multiplier: float,
    iqr_slider_disabled: bool,
) -> go.Figure:
    df = pd.DataFrame(data)

    filtered_df = df[df["year"].isin(selected_years)]
    outlier_group_by = "year"
    if selected_months:
        filtered_df = filtered_df[filtered_df["month"].isin(selected_months)]
        outlier_group_by = "month"

    x_axis = "md_label" if comparison_mode == "overlap" else "date"

    px_plot_func = px.line
    kwargs = {"color": "year", "markers": True}
    marker_dict = dict(size=3, color="orange")
    if plot_type == "scatter":
        px_plot_func = px.scatter
        kwargs = {
            "color": "price",
        }
        marker_dict = dict(
            size=6,
        )

    fig = px_plot_func(
        filtered_df,
        x=x_axis,
        y="price",
        custom_data=["date", "day_of_week"],
        color_discrete_sequence=px.colors.qualitative.Dark24,
        labels={x_axis: "Date", "price": "Price", "year": "Year"},
        title="Price Trend by Year",
        **kwargs,
    )

    fig.update_traces(
        marker=marker_dict,
        line=dict(width=2),
        hovertemplate=(
            "<b>Date:</b> %{customdata[0]|%m-%d}<br>"
            "<b>Day: </b>%{customdata[1]}<br>"
            "<b>Price:</b> %{y}<br>"
        ),
    )

    if not iqr_slider_disabled:
        outliers = detect_outlier_iqr(filtered_df, iqr_multiplier, outlier_group_by)
        if not outliers.empty:
            fig.add_scatter(
                x=outliers[x_axis],
                y=outliers["price"],
                mode="markers",
                marker=dict(size=11, symbol="circle-open"),
                name="Outlier",
                customdata=outliers[["date"]],
                hovertemplate=(
                    "Date: %{customdata[0]|%Y-%m-%d}<br>"
                    "Price: %{y}<br>"
                    "<extra>Outlier</extra>"
                ),
            )

    if period:
        for boundary in get_period_boundaries(period):
            fig.add_vline(
                x=boundary,
                line_width=1,
                line_dash="dot",
                line_color="blue",
                opacity=0.6,
            )
    fig.update_layout(template="plotly_white", hovermode="x unified")
    return fig
