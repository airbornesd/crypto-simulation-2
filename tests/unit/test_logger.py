from src.utils.logger import get_logger

logger = get_logger("test_logger")


def run_test():
    logger.info("logger test started")
    logger.warning("this is a warning")
    logger.error("this is an error log")
    print("check logs/app.log for entries")


if __name__ == "__main__":
    run_test()
