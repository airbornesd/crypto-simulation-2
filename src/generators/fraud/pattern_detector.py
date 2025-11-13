# src/generators/fraud/pattern_detector.py
import time
from src.utils.logger import get_logger
from src.utils.error_handler import safe_execute

logger = get_logger("pattern_detector")


def detect_fraudulent_pattern(trade: dict) -> dict:
    """
    simple heuristic-based fraud detector.
    looks for unusually large trades, fast repeats, or abnormal ratios.
    """
    try:
        risk_flags = []
        risk_score = 0.0

        if trade.get("total_value", 0) > 50000:
            risk_flags.append("high_value_trade")
            risk_score += 0.4

        if trade.get("quantity", 0) > 1:
            risk_flags.append("unusual_volume")
            risk_score += 0.2

        if trade.get("side") == "buy" and trade.get("price", 0) > 55000:
            risk_flags.append("overpriced_buy")
            risk_score += 0.3

        result = {
            "trade_id": trade.get("trade_id"),
            "user_id": trade.get("user_id"),
            "timestamp": int(time.time()),
            "risk_score": round(min(risk_score, 1.0), 2),
            "flags": risk_flags,
            "is_suspicious": risk_score >= 0.5,
            "source": "pattern_detector",
        }

        logger.info(
            f"fraud check for {trade.get('trade_id')}: {result['is_suspicious']}"
        )
        return result

    except Exception as e:
        logger.error(f"error detecting fraud: {e}")
        return None


def safe_detect_fraudulent_pattern(trade: dict):
    return safe_execute(detect_fraudulent_pattern, trade)
