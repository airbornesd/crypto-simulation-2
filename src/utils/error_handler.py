import time
from src.utils.logger import get_logger

logger = get_logger("utils_error_handler")


def safe_execute(func, *args, retries=3, delay=1, **kwargs):
    """
    safely execute a function with retries and error logging.
    if it fails after retries, logs and returns None.
    """

    for attempt in range(1, retries + 1):
        try:
            return func(*args, **kwargs)

        except Exception as e:
            logger.error(f"attempt {attempt} failed: {e}")

            if attempt < retries:
                time.sleep(delay)
            else:
                logger.error(
                    f"function {func.__name__} failed after {retries} attempts"
                )
                return None
