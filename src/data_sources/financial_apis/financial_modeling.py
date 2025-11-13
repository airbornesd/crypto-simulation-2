import requests
from src.utils.logger import get_logger
from src.utils.error_handler import safe_execute
from src.utils.config_loader import get_env

logger = get_logger("financial_modeling")

BASE_URL = get_env("FMP_URL", "https://financialmodelingprep.com/api/v3")
API_KEY = get_env("FMP_API_KEY", "")


def fetch_stock_quote(symbol="AAPL"):
    """
    fetch quote from financial modeling prep api.
    """
    try:
        url = f"{BASE_URL}/quote/{symbol}"
        params = {"apikey": API_KEY}
        resp = requests.get(url, params=params, timeout=5)
        resp.raise_for_status()
        data = resp.json()[0]

        parsed = {
            "symbol": data["symbol"],
            "price": data["price"],
            "change": data["changesPercentage"],
            "source": "financial_modeling",
        }

        logger.info(f"fetched quote for {symbol}: {data['price']}")
        return parsed

    except Exception as e:
        logger.error(f"error fetching {symbol} from FMP: {e}")
        return None


def safe_fetch_stock_quote(symbol="AAPL"):
    return safe_execute(fetch_stock_quote, symbol)
