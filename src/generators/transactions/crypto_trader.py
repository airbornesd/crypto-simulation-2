import time
import random
from src.utils.logger import get_logger
from src.utils.error_handler import safe_execute
from src.utils.config_loader import load_yaml_config
from src.producers.topic_manager import create_topics
from src.producers.kafka_producer import create_producer, send_event

logger = get_logger("start_generator")


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


def produce_crypto_trades(config_path="src/config/kafka_config.yaml"):
    """
    continuously produce crypto trades to kafka.
    """
    cfg = load_yaml_config(config_path)
    topic = "crypto_trades"

    # ensure topics exist
    create_topics(config_path)

    # initialize producer
    producer = create_producer(config_path)
    if not producer:
        logger.error("producer initialization failed — exiting")
        return

    users = [f"user_{i}" for i in range(1, 6)]

    logger.info("starting crypto trade stream ...")

    while True:
        user = random.choice(users)
        trade = safe_generate_crypto_trade(user)

        if trade:
            send_event(producer, topic, trade)
        else:
            logger.warning(f"failed to generate trade for {user}")

        time.sleep(random.uniform(0.5, 2.0))  # adjustable rate


if __name__ == "__main__":
    produce_crypto_trades()
