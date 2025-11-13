from src.generators.transactions.crypto_trader import safe_generate_crypto_trade
from src.generators.transactions.gold_trader import safe_generate_gold_trade
from src.generators.transactions.portfolio_manager import (
    safe_generate_portfolio_snapshot,
)
from src.generators.users.user_generator import safe_generate_user
from src.utils.logger import get_logger

logger = get_logger("test_transaction_generators")


def run_test():
    user = safe_generate_user()
    if not user:
        logger.error("user generation failed")
        return

    uid = user["user_id"]

    crypto_trade = safe_generate_crypto_trade(uid)
    gold_trade = safe_generate_gold_trade(uid)
    portfolio = safe_generate_portfolio_snapshot(uid)

    logger.info(f"user: {uid}")
    logger.info(f"crypto trade: {crypto_trade}")
    logger.info(f"gold trade: {gold_trade}")
    logger.info(f"portfolio: {portfolio}")


if __name__ == "__main__":
    run_test()
