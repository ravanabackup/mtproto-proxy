import requests
from src.models import ProxyMetrics
from src.render import MarkdownReadmeBuilder, TelegramMessageBuilder
from src import config


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
    if not config.TELEGRAM_BOT_TOKEN or not config.TELEGRAM_CHAT_ID:
        print("[Telegram] Bot is not configured, notification passed")
        return
    
    message = (
        TelegramMessageBuilder()
        .add_title()
        .add_stats(stats)
        .add_top_links(stats.valid, limit=20)
        .add_footer()
        .build()
    )

    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }

    for chat_id in config.TELEGRAM_CHAT_ID:
        payload["chat_id"] = chat_id
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            print("[Telegram] Notification has been sent")
        except Exception as e:
            print("[Telegram] Notification send error:", e)

    

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