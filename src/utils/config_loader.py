import os
import yaml
from pathlib import Path
from dotenv import load_dotenv
from src.utils.logger import get_logger

logger = get_logger("config_loader")

load_dotenv()


def get_env(key: str, default: str = None):
    """
    get environment variable safely.
    """
    value = os.getenv(key, default)

    if value is None:
        logger.warning(f"environment variable {key} not found, using default")
    return value


def load_yaml_config(path: str):
    """
    load yaml config file safely.
    """
    try:
        with open(Path(path), "r") as f:
            config = yaml.safe_load(f)
        logger.info(f"loaded config from {path}")
        return config or {}

    except FileNotFoundError:
        logger.error(f"config file not found: {path}")
        return {}

    except yaml.YAMLError as e:
        logger.error(f"yaml parse error in {path}: {e}")
        return {}
