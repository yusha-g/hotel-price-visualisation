from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = BASE_DIR / "assets"
DATA_FILE = ASSETS_DIR / "multi_year_price_data.csv"
