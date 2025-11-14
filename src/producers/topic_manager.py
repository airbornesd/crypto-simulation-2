from kafka.admin import KafkaAdminClient, NewTopic
from src.utils.logger import get_logger
from src.utils.error_handler import safe_execute
from src.utils.config_loader import load_yaml_config

logger = get_logger("topic_manager")


def create_topics(config_path: str):
    """
    create kafka topics defined in yaml config.
    """
    cfg = load_yaml_config(config_path)
    if not cfg or "bootstrap_servers" not in cfg:
        logger.error("invalid kafka config: missing bootstrap_servers")
        return False

    admin = safe_execute(KafkaAdminClient, bootstrap_servers=cfg["bootstrap_servers"])
    if not admin:
        logger.error("failed to initialize kafka admin client")
        return False

    existing_topics = safe_execute(admin.list_topics)
    if existing_topics is None:
        logger.error("failed to fetch existing topics")
        return False

    topics_to_create = []
    for topic_cfg in cfg.get("topics", []):
        topic_name = topic_cfg.get("name")
        if not topic_name:
            logger.warning("skipping unnamed topic entry in config")
            continue

        if topic_name not in existing_topics:
            new_topic = NewTopic(
                name=topic_name,
                num_partitions=topic_cfg.get("partitions", 3),
                replication_factor=topic_cfg.get("replication_factor", 1),
            )
            topics_to_create.append(new_topic)
        else:
            logger.info(f"topic already exists: {topic_name}")

    if topics_to_create:
        safe_execute(admin.create_topics, topics=topics_to_create)
        for t in topics_to_create:
            logger.info(f"created topic: {t.name}")

    admin.close()
    return True
