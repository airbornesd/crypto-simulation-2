# tests/unit/test_coin_gecko_client.py
from src.data_sources.crypto_exchanges.coingecko_client import (
    safe_fetch_coin_gecko_prices,
)
from src.utils.logger import get_logger

logger = get_logger("test_coin_gecko_client")


def run_test():
    logger.info("testing coingecko client")
    data = safe_fetch_coin_gecko_prices("usd", ["bitcoin", "ethereum"])
    if data:
        logger.info(f"fetched {len(data)} prices successfully")
    else:
        logger.warning("failed to fetch prices")


if __name__ == "__main__":
    run_test()
