# src/generators/fraud/anomaly_generator.py
import random
import time
from src.utils.logger import get_logger
from src.utils.error_handler import safe_execute

logger = get_logger("anomaly_generator")


def generate_anomalous_trade(user_id: str) -> dict:
    """
    create synthetic anomalous trade events.
    used to test data validation, schema robustness, and fraud systems.
    """
    try:
        anomaly_type = random.choice(
            ["negative_price", "massive_quantity", "missing_fields", "future_timestamp"]
        )

        trade_id = f"anomaly_{int(time.time() * 1000)}"
        base_data = {
            "trade_id": trade_id,
            "user_id": user_id,
            "symbol": random.choice(["BTCUSDT", "ETHUSDT", "XAUUSD"]),
            "timestamp": int(time.time()),
            "source": "anomaly_generator",
        }

        if anomaly_type == "negative_price":
            base_data.update(
                {
                    "price": -random.uniform(1000, 30000),
                    "quantity": random.uniform(0.01, 1.0),
                    "side": "buy",
                }
            )

        elif anomaly_type == "massive_quantity":
            base_data.update(
                {
                    "price": random.uniform(1000, 30000),
                    "quantity": random.uniform(100, 10000),
                    "side": "sell",
                }
            )

        elif anomaly_type == "missing_fields":
            # deliberately remove key fields
            base_data.update({"price": None, "side": None})

        elif anomaly_type == "future_timestamp":
            base_data.update(
                {
                    "price": random.uniform(1000, 30000),
                    "quantity": random.uniform(0.1, 1.0),
                    "side": "buy",
                    "timestamp": int(time.time()) + 86400,  # 1 day ahead
                }
            )

        base_data["anomaly_type"] = anomaly_type

        logger.warning(f"generated {anomaly_type} anomaly for {user_id}")
        return base_data

    except Exception as e:
        logger.error(f"error generating anomaly: {e}")
        return None


def safe_generate_anomalous_trade(user_id: str):
    return safe_execute(generate_anomalous_trade, user_id)
