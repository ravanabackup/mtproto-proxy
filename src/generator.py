from models import ProxyMetrics
from render import MarkdownReadmeBuilder
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