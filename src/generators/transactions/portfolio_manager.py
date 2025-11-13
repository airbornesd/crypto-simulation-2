import random
import time
from src.utils.logger import get_logger
from src.utils.error_handler import safe_execute

logger = get_logger("portfolio_manager")


def generate_portfolio_snapshot(user_id: str) -> dict:
    """
    simulate a user's portfolio snapshot.
    includes total assets, holdings, and risk metrics.
    """
    try:
        total_value = round(random.uniform(1000, 50000), 2)
        crypto_weight = round(random.uniform(0.4, 0.8), 2)
        gold_weight = round(1 - crypto_weight, 2)
        risk_index = round(random.uniform(0, 1), 2)

        data = {
            "user_id": user_id,
            "timestamp": int(time.time()),
            "total_value_usd": total_value,
            "weights": {"crypto": crypto_weight, "gold": gold_weight},
            "risk_index": risk_index,
            "source": "portfolio_manager",
        }

        logger.info(f"portfolio snapshot for {user_id}: ${total_value}")
        return data

    except Exception as e:
        logger.error(f"error generating portfolio for {user_id}: {e}")
        return None


def safe_generate_portfolio_snapshot(user_id: str):
    return safe_execute(generate_portfolio_snapshot, user_id)
