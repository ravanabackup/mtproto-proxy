from src.models import ProxyMetrics
from src.render import MarkdownReadmeBuilder, TelegramMessageBuilder
from src import config
from src.telegram_client import TelegramClient
from src.utils import evaluate_proxy_rate, ProxyRateEvaluation


def calculate_metrics(raw_count: int, valid_data: list[dict]) -> ProxyMetrics:
    alive_count = len(valid_data)
    dead_count = raw_count - alive_count

    avg_latency = (
        round(
            sum(
                p["latency_ms"]
                for p in valid_data
            ) / alive_count, 2
        )
        if alive_count
        else 0
    )

    rate = (
        round((alive_count / raw_count * 100), 1)
        if raw_count
        else 0.0
    )

    return ProxyMetrics(
        total=raw_count,
        valid=valid_data,
        alive_count=alive_count,
        dead_count=dead_count,
        avg_latency=avg_latency,
        rate=rate
    )


def send_telegram_notification(stats: ProxyMetrics):
    telegram = TelegramClient(token=config.TELEGRAM_BOT_TOKEN)
    message = (
        TelegramMessageBuilder()
        .add_title()
        .add_stats(stats)
        .add_top_links(stats.valid, limit=20)
        .add_footer()
        .build()
    )

    telegram.broadcast(
        chat_ids=config.TELEGRAM_CHAT_ID,
        text=message,
    )

    evaluation = evaluate_proxy_rate(stats)
    if evaluation == ProxyRateEvaluation.BAD:
        telegram.send_message(
            chat_id=config.TELEGRAM_BOT_OWNER_ID,
            text=(
                f"⚠ *Attention*\n"
                f"The proxy rate is low at `{stats.rate}%`. _({evaluation.value})_."
                "Please update the proxy list immediately!"
            )
        )

    telegram.close()


def generate_readme(stats: ProxyMetrics):
    readme = (
        MarkdownReadmeBuilder()
            .add_header()
            .add_downloads_block()
            .add_stats_table(stats)
            .add_top_proxies(stats.valid, limit=20)
            .build()
    )

    with open(config.README_PATH, "w", encoding="utf-8") as file:
        file.write(readme)