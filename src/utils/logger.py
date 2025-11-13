import logging
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FILE = os.getenv("LOG_FILE", "logs/app.log")

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)


def get_logger(name: str):
    """
    simple logger setup for consistent logs across modules
    logs go to both console and file.
    """

    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    # avoid duplicate handlers if already configured
    if logger.hasHandlers():
        return logger

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # file handler
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
