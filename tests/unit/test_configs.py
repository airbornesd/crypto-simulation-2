from src.utils.config_loader import get_env, load_yaml_config
from src.utils.logger import get_logger

logger = get_logger("test_config_loader")


def run_test():
    config = load_yaml_config("config/apis.yaml")
    logger.info(f"loaded config keys: {list(config.keys())}")

    base_url = get_env("BINANCE_BASE_URL")
    logger.info(f"env variable BINANCE_BASE_URL = {base_url}")


if __name__ == "__main__":
    run_test()
