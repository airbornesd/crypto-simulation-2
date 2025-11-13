import requests
from src.utils.logger import get_logger
from src.utils.error_handler import safe_execute
from src.utils.config_loader import load_yaml_config, get_env

logger = get_logger("coingecko_client")

CONFIG_PATH = "config/apis.yaml"
config = load_yaml_config(CONFIG_PATH)

BASE_URL = get_env(
    "COIN_GECKO_BASE_URL",
    config.get("coin_gecko", {}).get("base_url", "https://api.coingecko.com/api/v3"),
)
MARKETS_ENDPOINT = (
    config.get("coin_gecko", {}).get("endpoints", {}).get("markets", "/coins/markets")
)


def fetch_coin_gecko_prices(vs_currency="usd", symbols=None):
    """
    fetch crypto prices from coin gecko.
    symbols is a list of coin ids (['bitcoin', 'ethereum'])
    """
    try:
        url = f"{BASE_URL}{MARKETS_ENDPOINT}"
        params = {
            "vs_currency": vs_currency,
            "ids": ",".join(symbols) if symbols else "bitcoin,ethereum,solana",
        }
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        parsed = [
            {
                "symbol": coin["symbol"].upper(),
                "price": coin["current_price"],
                "source": "coingecko",
            }
            for coin in data
        ]

        logger.info(f"fetched {len(parsed)} prices successfully from coingecko")
        return parsed

    except requests.exceptions.RequestException as e:
        logger.error(f"network error while fetching coingecko data: {e}")
    except Exception as e:
        logger.error(f"unexpected error in coin_gecko_client: {e}")

    return None


def safe_fetch_coin_gecko_prices(vs_currency="usd", symbols=None):
    return safe_execute(fetch_coin_gecko_prices, vs_currency, symbols)
