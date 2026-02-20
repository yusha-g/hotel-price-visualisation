from dash import Dash, html, dcc

from hotel_price_visualisation.layout import build_layout
from hotel_price_visualisation.utils.data import load_and_prepare_data
import hotel_price_visualisation.callbacks  # noqa: F401


def create_app() -> Dash:
    app = Dash(__name__)

    df = load_and_prepare_data()
    app.layout = html.Div(
        [
            html.H2("Price Trend Comparison by Year"),
            dcc.Store(id="data-store", data=df.to_dict("records")),
            build_layout(df),
        ]
    )

    return app


app = create_app()
server = app.server

if __name__ == "__main__":
    app.run(
        debug=False,
        use_reloader=True,
    )
