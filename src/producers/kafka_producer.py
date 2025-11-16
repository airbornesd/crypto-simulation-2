import json
import time
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable, KafkaError
from src.utils.logger import get_logger
from src.utils.error_handler import safe_execute
from src.utils.config_loader import get_env

logger = get_logger("kafka_producer")


def wait_for_kafka(broker, max_retries=30, retry_delay=2):
    """
    wait for kafka to be available before connecting.
    """
    for attempt in range(1, max_retries + 1):
        try:
            # try to create a producer - if it succeeds, kafka is ready
            test_producer = KafkaProducer(
                bootstrap_servers=[broker],
                request_timeout_ms=5000,
                connections_max_idle_ms=10000,
            )
            test_producer.close()
            logger.info(f"kafka is ready at {broker}")
            return True
        except (NoBrokersAvailable, KafkaError) as e:
            if attempt < max_retries:
                logger.info(f"waiting for kafka... (attempt {attempt}/{max_retries})")
                time.sleep(retry_delay)
            else:
                logger.error(f"kafka not available after {max_retries} attempts: {e}")
                return False
        except Exception as e:
            logger.warning(f"unexpected error while checking kafka: {e}")
            if attempt < max_retries:
                time.sleep(retry_delay)
            else:
                return False
    return False


def get_kafka_producer(max_retries=5, retry_delay=2):
    """
    create and return a kafka producer with retry logic.
    """
    broker = get_env("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

    # wait for kafka to be ready
    if not wait_for_kafka(broker, max_retries=30, retry_delay=retry_delay):
        logger.error(f"kafka not available at {broker} after waiting")
        return None

    # now try to create the producer
    try:
        producer = KafkaProducer(
            bootstrap_servers=[broker],
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            key_serializer=lambda k: k.encode("utf-8") if k else None,
            linger_ms=10,
            retries=3,
            request_timeout_ms=10000,
            connections_max_idle_ms=10000,
        )
        logger.info(f"kafka producer connected to {broker}")
        return producer
    except Exception as e:
        logger.error(f"failed to create producer: {e}")
        return None


def send_to_kafka(producer, topic: str, key: str, value: dict):
    """
    send a message to kafka topic safely.
    """
    try:
        if producer:
            producer.send(topic, key=key, value=value)
            producer.flush()
            logger.info(f"sent event to {topic} | key={key}")
        else:
            logger.error("producer instance is None")
    except Exception as e:
        logger.error(f"failed to send event to {topic}: {e}")


def safe_send(producer, topic, key, value):
    """
    safely send a message to kafka with retry logic.
    """
    return safe_execute(send_to_kafka, producer, topic, key, value)
