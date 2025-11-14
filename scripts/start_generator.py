from src.producers.topic_manager import create_topics
from src.producers.kafka_producer import create_producer, send_event
from src.generators.transactions.crypto_trader import generate_trade

if __name__ == "__main__":
    create_topics("config/kafka_config.yaml")
    producer = create_producer()

    for _ in range(5):
        trade = generate_trade()
        send_event(producer, "crypto_trades", trade)
