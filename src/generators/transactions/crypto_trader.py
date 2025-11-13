import random
import time
from src.utils.logger import get_logger
from src.utils.error_handler import safe_execute

logger = get_logger("crypto_trader")


def generate_crypto_trade(user_id: str, symbols=None) -> dict:
    """
    simulate a crypto trade (buy/sell) for a user.
    """
    try:
        symbols = symbols or ["BTCUSDT", "ETHUSDT", "BNBUSDT"]
        trade_id = f"trade_{int(time.time() * 1000)}"
        symbol = random.choice(symbols)
        side = random.choice(["buy", "sell"])
        quantity = round(random.uniform(0.001, 1.5), 4)
        price = round(random.uniform(1000, 60000), 2)
        total_value = round(quantity * price, 2)

        data = {
            "trade_id": trade_id,
            "user_id": user_id,
            "symbol": symbol,
            "side": side,
            "quantity": quantity,
            "price": price,
            "total_value": total_value,
            "timestamp": int(time.time()),
            "source": "crypto_trader",
        }

        logger.info(
            f"generated {side} trade for {user_id} ({symbol} {quantity} @ {price})"
        )
        return data

    except Exception as e:
        logger.error(f"error generating crypto trade for {user_id}: {e}")
        return None


def safe_generate_crypto_trade(user_id: str, symbols=None):
    return safe_execute(generate_crypto_trade, user_id, symbols)
