# src/generators/transactions/gold_trader.py
import random
import time
from src.utils.logger import get_logger
from src.utils.error_handler import safe_execute

logger = get_logger("gold_trader")


def generate_gold_trade(user_id: str) -> dict:
    """
    simulate a gold trade (buy/sell) for a user.
    """
    try:
        trade_id = f"gold_{int(time.time() * 1000)}"
        side = random.choice(["buy", "sell"])
        quantity_oz = round(random.uniform(0.1, 5.0), 3)
        price_per_oz = round(random.uniform(1800, 2100), 2)
        total_value = round(quantity_oz * price_per_oz, 2)

        data = {
            "trade_id": trade_id,
            "user_id": user_id,
            "asset": "GOLD",
            "side": side,
            "quantity_oz": quantity_oz,
            "price_per_oz": price_per_oz,
            "total_value": total_value,
            "timestamp": int(time.time()),
            "source": "gold_trader",
        }

        logger.info(f"generated {side} gold trade for {user_id}")
        return data

    except Exception as e:
        logger.error(f"error generating gold trade for {user_id}: {e}")
        return None


def safe_generate_gold_trade(user_id: str):
    return safe_execute(generate_gold_trade, user_id)
