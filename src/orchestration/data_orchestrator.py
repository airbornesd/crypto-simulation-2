import random
import time
from src.producers.kafka_producer import get_kafka_producer, send_to_kafka
from src.producers.topic_manager import get_topic
from src.generators.users.user_generator import safe_generate_user
from src.generators.transactions.crypto_trader import safe_generate_crypto_trade
from src.generators.transactions.gold_trader import safe_generate_gold_trade
from src.generators.fraud.pattern_detector import safe_detect_fraudulent_pattern
from src.utils.logger import get_logger

logger = get_logger("data_orchestrator")


def run_data_stream():
    """
    main loop: generate and push data to kafka topics.
    """
    producer = get_kafka_producer()
    if not producer:
        logger.error("cannot start orchestrator: kafka unavailable")
        return

    while True:
        try:
            # randomly pick an event type
            event_type = random.choice(["user", "crypto", "gold", "fraud"])

            if event_type == "user":
                user = safe_generate_user()
                send_to_kafka(producer, get_topic("users"), user["user_id"], user)

            elif event_type == "crypto":
                user_id = f"user_{random.randint(1000, 9999)}"
                trade = safe_generate_crypto_trade(user_id)
                send_to_kafka(producer, get_topic("crypto"), trade["trade_id"], trade)

            elif event_type == "gold":
                user_id = f"user_{random.randint(1000, 9999)}"
                trade = safe_generate_gold_trade(user_id)
                send_to_kafka(producer, get_topic("gold"), trade["trade_id"], trade)

            elif event_type == "fraud":
                fake_trade = safe_generate_crypto_trade(
                    f"user_{random.randint(1000, 9999)}"
                )
                fraud_result = safe_detect_fraudulent_pattern(fake_trade)
                send_to_kafka(
                    producer, get_topic("fraud"), fraud_result["trade_id"], fraud_result
                )

            time.sleep(random.uniform(0.5, 2.0))

        except KeyboardInterrupt:
            logger.info("orchestrator stopped manually")
            break
        except Exception as e:
            logger.error(f"error in orchestrator loop: {e}")
