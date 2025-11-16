import random
import time
from src.utils.logger import get_logger
from src.utils.error_handler import safe_execute_decorator
from src.producers.kafka_producer import get_kafka_producer, send_to_kafka
from src.producers.topic_manager import get_topic
from src.generators.users.user_generator import safe_generate_user
from src.generators.transactions.crypto_trader import safe_generate_crypto_trade
from src.generators.transactions.gold_trader import safe_generate_gold_trade
from src.generators.transactions.portfolio_manager import (
    safe_generate_portfolio_snapshot,
)
from src.generators.fraud.pattern_detector import safe_detect_fraudulent_pattern

logger = get_logger("start_generator")


@safe_execute_decorator
def generate_and_stream():
    """
    continuously generate fintech data and stream to kafka topics.
    """
    producer = get_kafka_producer()
    if not producer:
        logger.error("unable to connect to kafka broker, exiting...")
        return

    logger.info("fintech data generator started.")
    logger.info("streaming data to kafka topics...")

    try:
        while True:
            event_type = random.choice(["user", "crypto", "gold", "fraud", "portfolio"])

            if event_type == "user":
                user = safe_generate_user()
                if user:
                    send_to_kafka(producer, get_topic("users"), user["user_id"], user)

            elif event_type == "crypto":
                user_id = f"user_{random.randint(1000, 9999)}"
                trade = safe_generate_crypto_trade(user_id)
                if trade:
                    send_to_kafka(
                        producer, get_topic("crypto"), trade["trade_id"], trade
                    )

            elif event_type == "gold":
                user_id = f"user_{random.randint(1000, 9999)}"
                trade = safe_generate_gold_trade(user_id)
                if trade:
                    send_to_kafka(producer, get_topic("gold"), trade["trade_id"], trade)

            elif event_type == "portfolio":
                user_id = f"user_{random.randint(1000, 9999)}"
                portfolio = safe_generate_portfolio_snapshot(user_id)
                if portfolio:
                    send_to_kafka(
                        producer,
                        get_topic("portfolio"),
                        portfolio["user_id"],
                        portfolio,
                    )

            elif event_type == "fraud":
                fake_trade = safe_generate_crypto_trade(
                    f"user_{random.randint(1000, 9999)}"
                )
                fraud_result = safe_detect_fraudulent_pattern(fake_trade)
                if fraud_result:
                    send_to_kafka(
                        producer,
                        get_topic("fraud"),
                        fraud_result["trade_id"],
                        fraud_result,
                    )

            time.sleep(random.uniform(0.5, 2.0))

    except KeyboardInterrupt:
        logger.info("generator interrupted manually.")
    except Exception as e:
        logger.error(f"error in generator loop: {e}")
    finally:
        logger.info("shutting down producer...")
        producer.close()


if __name__ == "__main__":
    generate_and_stream()
