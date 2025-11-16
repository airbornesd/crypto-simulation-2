import time
from functools import wraps
from src.utils.logger import get_logger

logger = get_logger("utils_error_handler")


def safe_execute(func, *args, retries=3, delay=1, **kwargs):
    """
    safely execute a function with retries and error logging.

    Usage:
    - As a function call: safe_execute(func, arg1, arg2, retries=3)
    - As a decorator: Use @safe_execute_decorator instead

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


def safe_execute_decorator(func=None, *, retries=3, delay=1):
    """
    Decorator version of safe_execute.

    Usage:
    @safe_execute_decorator
    def my_function():
        pass

    @safe_execute_decorator(retries=5, delay=2)
    def my_function():
        pass
    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            result = safe_execute(f, *args, retries=retries, delay=delay, **kwargs)
            # Ensure we always return something, even if None
            return result

        return wrapper

    if func is None:
        # Called as @safe_execute_decorator(retries=5) or @safe_execute_decorator()
        return decorator
    else:
        # Called as @safe_execute_decorator
        return decorator(func)
