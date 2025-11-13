from src.data_sources.metals.gold_api import safe_fetch_gold_price
from src.utils.logger import get_logger

logger = get_logger("test_gold_api")


def run_test():
    logger.info("testing gold api simulator")
    data = safe_fetch_gold_price()
    if data:
        logger.info(f"gold price fetched successfully: {data}")
    else:
        logger.warning("failed to fetch gold price")


if __name__ == "__main__":
    run_test()
