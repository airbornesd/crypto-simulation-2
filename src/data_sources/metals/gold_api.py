# src/data_sources/metals/gold_api.py
import random
import time
from src.utils.logger import get_logger
from src.utils.error_handler import safe_execute

logger = get_logger("gold_api")


def fetch_gold_price() -> dict:
    """
    simulate fetching gold price.
    we generate a pseudo-random price around 2000 ± small variation.
    """
    try:
        base_price = 2000.0
        variation = random.uniform(-5, 5)
        price = round(base_price + variation, 2)

        data = {
            "symbol": "XAUUSD",
            "price": price,
            "timestamp": int(time.time()),
            "source": "simulated_gold_api",
        }

        logger.info(f"fetched gold price: {price}")
        return data

    except Exception as e:
        logger.error(f"error simulating gold price: {e}")
        return None


def safe_fetch_gold_price():
    return safe_execute(fetch_gold_price)
