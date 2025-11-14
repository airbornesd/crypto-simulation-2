import json
from kafka import KafkaProducer
from src.utils.logger import get_logger
from src.utils.error_handler import safe_execute
from src.utils.config_loader import load_yaml_config

logger = get_logger("kafka_producer")


def create_producer(config_path="src/config/kafka_config.yaml"):
    """
    initialize kafka producer using loaded config.
    """
    cfg = load_yaml_config(config_path)
    if not cfg or "bootstrap_servers" not in cfg:
        logger.error("invalid kafka config: missing bootstrap_servers")
        return None

    producer = safe_execute(
        KafkaProducer,
        bootstrap_servers=cfg["bootstrap_servers"],
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        acks=cfg.get("acks", "all"),
        retries=cfg.get("retries", 3),
        linger_ms=cfg.get("linger_ms", 5),
        batch_size=cfg.get("batch_size", 32768),
    )

    if producer:
        logger.info("kafka producer initialized successfully")
    else:
        logger.error("failed to initialize kafka producer")

    return producer


def send_event(producer, topic: str, event: dict):
    """
    send event to kafka topic safely.
    """
    if not producer:
        logger.error("producer is not initialized")
        return False

    result = safe_execute(producer.send, topic, value=event)
    if result:
        logger.info(f"event sent to {topic}: {event}")
        return True
    else:
        logger.error(f"failed to send event to {topic}")
        return False
