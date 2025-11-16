TOPICS = {
    "crypto": "crypto_stream",
    "gold": "gold_stream",
    "users": "user_stream",
    "fraud": "fraud_stream",
    "portfolio": "portfolio_stream",
}


def get_topic(name: str) -> str:
    """
    return topic name for given alias.
    """
    return TOPICS.get(name.lower(), "misc_stream")


def list_topics() -> list:
    """
    return all registered topics.
    """
    return list(TOPICS.values())
