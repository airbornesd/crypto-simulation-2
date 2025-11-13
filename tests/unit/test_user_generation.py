from src.generators.users.user_generator import safe_generate_user
from src.generators.users.kyc_generator import safe_generate_kyc_record
from src.utils.logger import get_logger

logger = get_logger("test_user_generation")


def run_test():
    logger.info("testing user + kyc generators")
    user = safe_generate_user()
    if not user:
        logger.error("failed to generate user")
        return

    kyc = safe_generate_kyc_record(user["user_id"])
    logger.info(f"user: {user}")
    logger.info(f"kyc: {kyc}")


if __name__ == "__main__":
    run_test()
