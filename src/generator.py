from models import ProxyMetrics
from render import MarkdownReadmeBuilder
from src import config


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