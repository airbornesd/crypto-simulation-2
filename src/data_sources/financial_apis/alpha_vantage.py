# src/data_sources/financial_apis/alpha_vantage.py
import requests
from src.utils.logger import get_logger
from src.utils.error_handler import safe_execute
from src.utils.config_loader import get_env

logger = get_logger("alpha_vantage")

API_KEY = get_env("ALPHA_VANTAGE_KEY")
BASE_URL = get_env("ALPHA_VANTAGE_URL", "https://www.alphavantage.co/query")


def fetch_stock_price(symbol="IBM"):
    """
    fetch stock price using alpha vantage (TIME_SERIES_INTRADAY).
    """
    try:
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": symbol,
            "interval": "1min",
            "apikey": API_KEY,
        }
        resp = requests.get(BASE_URL, params=params, timeout=5)
        resp.raise_for_status()
        data = resp.json()

        # grab the latest available entry
        series = data.get("Time Series (1min)")
        if not series:
            logger.warning(f"no intraday data for {symbol}")
            return None

        latest_time = sorted(series.keys())[-1]
        price = float(series[latest_time]["1. open"])

        parsed = {
            "symbol": symbol,
            "price": price,
            "timestamp": latest_time,
            "source": "alpha_vantage",
        }

        logger.info(f"fetched {symbol} price from alpha vantage: {price}")
        return parsed

    except Exception as e:
        logger.error(f"error fetching {symbol} from alpha vantage: {e}")
        return None


def safe_fetch_stock_price(symbol="IBM"):
    return safe_execute(fetch_stock_price, symbol)
