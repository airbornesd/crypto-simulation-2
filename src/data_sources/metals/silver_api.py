import random
import time
from src.utils.logger import get_logger
from src.utils.error_handler import safe_execute

logger = get_logger("silver_api")


def fetch_silver_price() -> dict:
    """
    simulate silver price feed.
    price hovers around $25 ± 0.5.
    """
    try:
        base_price = 25.0
        variation = random.uniform(-0.5, 0.5)
        price = round(base_price + variation, 3)

        data = {
            "symbol": "XAGUSD",
            "price": price,
            "timestamp": int(time.time()),
            "source": "simulated_silver_api",
        }

        logger.info(f"fetched silver price: {price}")
        return data

    except Exception as e:
        logger.error(f"error simulating silver price: {e}")
        return None


def safe_fetch_silver_price():
    return safe_execute(fetch_silver_price)
