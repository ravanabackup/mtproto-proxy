import pytest
from src.telegram_client import TelegramClient
from src.config import TELEGRAM_BOT_TOKEN, TELEGRAM_BOT_OWNER_ID
from src.utils import ProxyRateEvaluation, evaluate_proxy_rate
from src.models import ProxyMetrics


def test_send_message_low_rate():
    telegram = TelegramClient(token=TELEGRAM_BOT_TOKEN)
    fake_stats_low_rate = ProxyMetrics(
        total=200,
        alive_count=50,
        avg_latency=234.5,
        dead_count=2,
        rate=44.9,
        valid=None 
    )

    evaluation = evaluate_proxy_rate(fake_stats_low_rate)

    if evaluation == ProxyRateEvaluation.BAD:
        result = telegram.send_message(
            chat_id=TELEGRAM_BOT_OWNER_ID,
            text=(
                f"⚠ *Attention*\n"
                f"The proxy rate is low at `{fake_stats_low_rate.rate}%` _({evaluation.value})_. "
                "Please update the proxy list immediately!"
            )
        )

        assert evaluation is ProxyRateEvaluation.BAD
        assert result is True