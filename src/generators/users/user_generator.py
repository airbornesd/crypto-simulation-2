import random
import time
from faker import Faker
from src.utils.logger import get_logger
from src.utils.error_handler import safe_execute

logger = get_logger("user_generator")
fake = Faker()


def generate_user() -> dict:
    """
    generate a random user profile with basic details.
    """
    try:
        user_id = f"user_{random.randint(1000, 9999)}"
        country = random.choice(["IN", "US", "UK", "DE", "SG"])
        account_type = random.choice(["basic", "premium", "institutional"])
        created_at = int(time.time())

        data = {
            "user_id": user_id,
            "name": fake.name(),
            "email": fake.email(),
            "country": country,
            "account_type": account_type,
            "balance_usd": round(random.uniform(100, 10000), 2),
            "risk_score": round(random.uniform(0, 1), 2),
            "created_at": created_at,
            "source": "user_generator",
        }

        logger.info(f"generated user: {user_id}")
        return data

    except Exception as e:
        logger.error(f"error generating user: {e}")
        return None


def safe_generate_user():
    return safe_execute(generate_user)
