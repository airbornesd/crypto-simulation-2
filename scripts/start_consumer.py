try:
    from src.consumers.kafka_consumer import start_consumer
except Exception as e:
    raise ImportError(f"Failed to import start_consumer: {e}")

if __name__ == "__main__":
    if not callable(start_consumer):
        raise TypeError(
            f"start_consumer is not callable (type: {type(start_consumer)}) - import may have failed"
        )
    start_consumer()
