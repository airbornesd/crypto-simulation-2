import random
import time
from src.utils.logger import get_logger
from src.utils.error_handler import safe_execute

logger = get_logger("kyc_generator")


def generate_kyc_record(user_id: str) -> dict:
    """
    generate kyc information for a given user id.
    """
    try:
        kyc_status = random.choice(["verified", "pending", "rejected"])
        kyc_score = (
            round(random.uniform(0.5, 1.0), 2) if kyc_status == "verified" else 0.0
        )
        document_type = random.choice(["passport", "aadhar", "driver_license"])
        verified_at = int(time.time()) if kyc_status == "verified" else None

        data = {
            "user_id": user_id,
            "kyc_status": kyc_status,
            "kyc_score": kyc_score,
            "document_type": document_type,
            "verified_at": verified_at,
            "source": "kyc_generator",
        }

        logger.info(f"generated kyc for {user_id} ({kyc_status})")
        return data

    except Exception as e:
        logger.error(f"error generating kyc for {user_id}: {e}")
        return None


def safe_generate_kyc_record(user_id: str):
    return safe_execute(generate_kyc_record, user_id)
