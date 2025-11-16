from src.producers.kafka_producer import get_kafka_producer, send_to_kafka
from src.producers.topic_manager import get_topic


def run_test():
    producer = get_kafka_producer()
    data = {"msg": "hello kafka", "timestamp": "test"}
    send_to_kafka(producer, get_topic("crypto"), "test_key", data)


if __name__ == "__main__":
    run_test()
