import requests
from src.utils.logger import get_logger
from src.utils.error_handler import safe_execute
from src.utils.config_loader import load_yaml_config, get_env

logger = get_logger("coinbase_client")

CONFIG_PATH = "config/real_apis.yaml"
config = load_yaml_config(CONFIG_PATH)

BASE_URL = get_env(
    "COINBASE_BASE_URL",
    config.get("coinbase", {}).get("base_url", "https://api.coinbase.com/v2"),
)
SPOT_ENDPOINT = (
    config.get("coinbase", {}).get("endpoints", {}).get("spot", "/prices/{pair}/spot")
)


def fetch_coinbase_price(pair="BTC-USD") -> dict:
    """
    fetch current spot price from coinbase.
    """
    try:
        url = f"{BASE_URL}{SPOT_ENDPOINT.replace('{pair}', pair)}"
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()["data"]

        parsed = {
            "symbol": data["base"],
            "currency": data["currency"],
            "price": float(data["amount"]),
            "source": "coinbase",
        }

        logger.info(f"fetched {pair} from coinbase: {parsed['price']}")
        return parsed

    except requests.exceptions.RequestException as e:
        logger.error(f"network error coinbase {pair}: {e}")
    except Exception as e:
        logger.error(f"unexpected error coinbase {pair}: {e}")
    return None


def safe_fetch_coinbase_price(pair="BTC-USD"):
    return safe_execute(fetch_coinbase_price, pair)
