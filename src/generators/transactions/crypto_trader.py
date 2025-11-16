import time
import random
from src.utils.logger import get_logger
from src.utils.error_handler import safe_execute
from src.producers.kafka_producer import get_kafka_producer, send_to_kafka
from src.producers.topic_manager import get_topic

logger = get_logger("crypto_trader")


def generate_crypto_trade(user_id: str, symbols=None) -> dict:
    """
    simulate a crypto trade (buy/sell) for a user.
    """
    symbols = symbols or ["BTCUSDT", "ETHUSDT", "BNBUSDT"]
    trade_id = f"trade_{int(time.time() * 1000)}"
    symbol = random.choice(symbols)
    side = random.choice(["buy", "sell"])
    quantity = round(random.uniform(0.001, 1.5), 4)
    price = round(random.uniform(1000, 60000), 2)
    total_value = round(quantity * price, 2)

    data = {
        "trade_id": trade_id,
        "user_id": user_id,
        "symbol": symbol,
        "side": side,
        "quantity": quantity,
        "price": price,
        "total_value": total_value,
        "timestamp": int(time.time()),
        "source": "crypto_trader",
    }

    logger.info(f"generated {side} trade for {user_id} ({symbol} {quantity} @ {price})")
    return data


def safe_generate_crypto_trade(user_id: str, symbols=None):
    """
    safely generate a trade event with retry.
    """
    return safe_execute(generate_crypto_trade, user_id, symbols)


def produce_crypto_trades():
    """
    continuously produce crypto trades to kafka.
    """
    topic = get_topic("crypto")

    # initialize producer
    producer = get_kafka_producer()
    if not producer:
        logger.error("producer initialization failed — exiting")
        return

    users = [f"user_{i}" for i in range(1, 6)]

    logger.info("starting crypto trade stream ...")

    try:
        while True:
            user = random.choice(users)
            trade = safe_generate_crypto_trade(user)

            if trade:
                send_to_kafka(
                    producer,
                    topic,
                    trade.get("trade_id", trade.get("user_id", "unknown")),
                    trade,
                )
            else:
                logger.warning(f"failed to generate trade for {user}")

            time.sleep(random.uniform(0.5, 2.0))  # adjustable rate
    except KeyboardInterrupt:
        logger.info("crypto trade stream interrupted")
    except Exception as e:
        logger.error(f"error in crypto trade stream: {e}")
    finally:
        if producer:
            producer.close()


if __name__ == "__main__":
    produce_crypto_trades()
