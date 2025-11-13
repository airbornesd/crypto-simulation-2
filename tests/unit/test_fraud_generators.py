from src.generators.fraud.pattern_detector import safe_detect_fraudulent_pattern
from src.generators.fraud.anomaly_generator import safe_generate_anomalous_trade
from src.generators.users.user_generator import safe_generate_user
from src.generators.transactions.crypto_trader import safe_generate_crypto_trade
from src.utils.logger import get_logger

logger = get_logger("test_fraud_generators")


def run_test():
    user = safe_generate_user()
    if not user:
        logger.error("failed to generate user")
        return

    uid = user["user_id"]

    # generate normal trade and analyze it
    normal_trade = safe_generate_crypto_trade(uid)
    fraud_result = safe_detect_fraudulent_pattern(normal_trade)

    # generate an anomaly for stress testing
    anomaly = safe_generate_anomalous_trade(uid)

    logger.info(f"fraud analysis: {fraud_result}")
    logger.warning(f"synthetic anomaly: {anomaly}")


if __name__ == "__main__":
    run_test()
