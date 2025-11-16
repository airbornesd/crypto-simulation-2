import json
import time
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
from src.utils.logger import get_logger
from src.utils.config_loader import get_env
from src.utils.error_handler import safe_execute_decorator
from src.consumers.sinks.parquet_sink import write_to_parquet
from datetime import datetime

logger = get_logger("kafka_consumer")


def create_consumer(topics=None, max_retries=10, retry_delay=3):
    """
    Create Kafka consumer with retry logic to wait for Kafka to be ready.
    """
    broker = get_env("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    topics = topics or [
        "crypto_stream",
        "gold_stream",
        "user_stream",
        "fraud_stream",
        "portfolio_stream",
    ]

    for attempt in range(1, max_retries + 1):
        try:
            consumer = KafkaConsumer(
                *topics,
                bootstrap_servers=[broker],
                auto_offset_reset="earliest",  # Changed to earliest to consume all messages
                enable_auto_commit=True,
                group_id="fintech_consumer_group",
                value_deserializer=lambda v: json.loads(v.decode("utf-8")),
                key_deserializer=lambda k: k.decode("utf-8") if k else None,
            )
            logger.info(f"connected to kafka broker: {broker}")
            logger.info(f"subscribed to topics: {topics}")
            return consumer
        except NoBrokersAvailable as e:
            if attempt < max_retries:
                logger.warning(
                    f"attempt {attempt}/{max_retries}: Kafka broker not available yet. "
                    f"Retrying in {retry_delay}s... ({e})"
                )
                time.sleep(retry_delay)
            else:
                logger.error(
                    f"failed to create kafka consumer after {max_retries} attempts: {e}"
                )
                raise
        except Exception as e:
            logger.error(f"failed to create kafka consumer: {e}")
            raise


def consume_and_persist(consumer, batch_size=50, flush_interval_seconds=30):
    """
    consume messages and periodically persist them to parquet.
    Flushes when batch size is reached or after flush_interval_seconds.
    """
    if not consumer:
        logger.error("consumer instance is None")
        return

    buffer = {}
    last_flush = datetime.utcnow()

    logger.info("starting message consumption and parquet persistence...")

    try:
        for msg in consumer:
            topic = msg.topic
            event = msg.value

            # add event to buffer
            buffer.setdefault(topic, []).append(event)

            current_time = datetime.utcnow()
            time_since_flush = (current_time - last_flush).total_seconds()

            # flush condition: batch size reached OR time interval exceeded
            should_flush = (
                len(buffer[topic]) >= batch_size
                or time_since_flush >= flush_interval_seconds
            )

            if should_flush:
                for topic_name, events in list(buffer.items()):
                    if events:
                        write_to_parquet(events, topic_name)
                        logger.info(
                            f"flushed {len(events)} events for topic {topic_name}"
                        )
                        buffer[topic_name].clear()
                last_flush = current_time

    except KeyboardInterrupt:
        logger.info("consumer stopped manually")
    except Exception as e:
        logger.error(f"error in consumer loop: {e}")
    finally:
        # flush remaining events
        for topic, events in buffer.items():
            if events:
                write_to_parquet(events, topic)
                logger.info(f"flushed remaining {len(events)} events for topic {topic}")
        consumer.close()
        logger.info("consumer connection closed")


@safe_execute_decorator
def start_consumer(topics=None):
    consumer = create_consumer(topics)
    consume_and_persist(consumer)
