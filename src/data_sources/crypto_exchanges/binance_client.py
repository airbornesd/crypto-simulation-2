import requests
import os
from src.utils.logger import get_logger
from src.utils.error_handler import safe_execute
from src.utils.config_loader import load_yaml_config, get_env

logger = get_logger("binance_client")

# load config
CONFIG_PATH = "config/apis.yaml"
config = load_yaml_config(CONFIG_PATH)

# resolve base url (prefer env override)
BASE_URL = get_env(
    "BINANCE_BASE_URL",
    config.get("binance", {}).get("base_url", "https://api.binance.com"),
)
TICKER_ENDPOINT = (
    config.get("binance", {}).get("endpoints", {}).get("ticker", "/api/v3/ticker/price")
)


def fetch_binance_price(symbol: str) -> dict:
    """
    fetches latest crypto price from binance public api.
    returns dict: {symbol, price, source}
    """
    try:
        url = f"{BASE_URL}{TICKER_ENDPOINT}"
        response = requests.get(url, params={"symbol": symbol}, timeout=5)
        response.raise_for_status()

        data = response.json()
        parsed = {
            "symbol": data["symbol"],
            "price": float(data["price"]),
            "source": "binance",
        }

        logger.info(f"fetched price successfully for {symbol}: {parsed['price']}")
        return parsed

    except requests.exceptions.Timeout:
        logger.error(f"timeout while fetching {symbol} from binance")
    except requests.exceptions.RequestException as e:
        logger.error(f"network error while fetching {symbol}: {e}")
    except (ValueError, KeyError) as e:
        logger.error(f"parse error for {symbol}: {e}")
    except Exception as e:
        logger.error(f"unexpected error for {symbol}: {e}")

    return None


def safe_fetch_binance_price(symbol: str):
    """
    wrapper using safe_execute for retry logic.
    """
    return safe_execute(fetch_binance_price, symbol)
