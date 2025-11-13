from src.data_sources.crypto_exchanges.binance_client import safe_fetch_binance_price
from src.utils.logger import get_logger

logger = get_logger("test_binance_client")


def run_test():
    logger.info("testing binance client fetch")
    result = safe_fetch_binance_price("BTCUSDT")

    if result:
        logger.info(f"binance result: {result}")
    else:
        logger.warning("failed to fetch binance price")


if __name__ == "__main__":
    run_test()
