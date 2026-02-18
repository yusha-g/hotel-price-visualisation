from pathlib import Path
from dash import Dash, Input, Output, html, dcc, Figure
import pandas as pd
import plotly.express as px

app = Dash(__name__)


def get_data() -> pd.DataFrame:
    filepath = Path(__file__).parents[1]
    filename = "multi_year_price_data.csv"
    return pd.read_csv(filepath / "assets" / filename)


def format_data(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.lower()
    df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y")
    df["year"] = df["date"].dt.year
    return df


df = format_data(get_data())


@app.callback(  # type: ignore[misc]
    Output("price-graph", "figure"), Input("year-dropdown", "value")
)
def update_graph(selected_years: list[int]) -> Figure:
    filtered_df = df[df["year"].isin(selected_years)]

    fig = px.line(
        filtered_df,
        x="date",
        y="price",
        color="year",
        labels={"date": "Date", "price": "Price", "year": "Year"},
        title="Price Trend by Year",
    )

    # fig.update_layout(xaxis_title="Date", yaxis_title="Price")
    return fig


def contruct_app_layout(df: pd.DataFrame) -> None:
    heading = html.H2("Price Trend Comparison by Year")
    year_dropdown = dcc.Dropdown(
        id="year-dropdown",
        options=[
            {"label": str(year), "value": year} for year in sorted(df["year"].unique())
        ],
        multi=True,
        value=[df["year"].min()],  # default selection
        placeholder="Select year(s)",
    )
    graph = dcc.Graph(id="price-graph")
    app.layout = html.Div([heading, year_dropdown, graph])


def main() -> None:
    contruct_app_layout(df)
    app.run(debug=True)


if __name__ == "__main__":
    main()
