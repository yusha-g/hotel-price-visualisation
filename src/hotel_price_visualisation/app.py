from dash import Dash

from layout import contruct_app_layout
from utils.data import load_and_prepare_data
import callbacks  # noqa: F401

app = Dash(__name__)


def main() -> None:
    df = load_and_prepare_data()
    app.layout = contruct_app_layout(df)
    app.run(
        debug=False,
        use_reloader=True,
    )


if __name__ == "__main__":
    main()
