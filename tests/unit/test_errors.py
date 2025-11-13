from src.utils.error_handler import safe_execute
from src.utils.logger import get_logger

logger = get_logger("test_error_handler")


def divide(a, b):
    return a / b


def run_test():
    logger.info("running safe_execute success case")
    safe_execute(divide, 10, 2)

    logger.info("running safe_execute failure case")
    safe_execute(divide, 10, 0)


if __name__ == "__main__":
    run_test()
