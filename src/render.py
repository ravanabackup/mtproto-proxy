from datetime import datetime, UTC
from src.models import ProxyMetrics


class MarkdownReadmeBuilder:
    def __init__(self) -> None:
        self._sections: list[str] = []

    
    def add_header(self) -> MarkdownReadmeBuilder:
        header = (
            "# MTProto Proxy 🌐\n"

            "> [!NOTE]\n"
            f"> **Last Update:** _{datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC')}_\n\n"

            "This repository provides auto-updating proxies "
            "for Telegram to help you bypass the messenger's "
            "restrictions in Russia 🇷🇺\n\n"

            "Proxies are updated every **2 hours**, after which "
            "tracking is conducted, which you can review below. "
            "Additionally, below you will find a table with "
            "the best ones and a link for instant connection\n\n"
        )

        self._sections.append(header)
        return self
    

    def add_downloads_block(self) -> MarkdownReadmeBuilder:
        downloads = (
            "### 📥 Download\n"
            
            "- 📄 [.TXT](https://github.com/shablin/mtproto-proxy/blob/main/data/valid_proxy.txt) (`data/valid_proxy.txt`)\n"
            "- 📄 [.JSON](https://github.com/shablin/mtproto-proxy/blob/main/data/valid_proxy.json) (`data/valid_proxy.json`)\n\n"

            "> [!WARNING]\n"
            "> At the moment, an imprecise method is used to measure latency.\n"
            "> This will be fixed in the future.\n"
            "> Also note that some proxies may be unavailable in your region\n"
        )

        self._sections.append(downloads)
        return self
    

    def add_stats_table(self, stats: ProxyMetrics) -> MarkdownReadmeBuilder:
        table = (
            "## 📊 Stats\n"
            "| 🔢 Total | 🟢 Alive | 🔴 Dead | ⚡ Avg. Latency | 📈 Rate |\n"
            "| :-------: | :------: | :-----: | :-------------: | :------: |\n"
            f"| {stats.total} | {stats.alive_count} |"
            f"{stats.dead_count} | {stats.avg_latency} ms | {stats.rate}% |"
        )

        self._sections.append(table)
        return self
    

    def add_top_proxies(self, valid_data: list[dict], limit: int = 20) -> MarkdownReadmeBuilder:
        table_header = (
            f"## 🌐 Top {limit} Fastest Proxies\n"
            "| 🖥️ Host | ⚡ Latency (ms) | 🔗 Link |\n"
            "| -------- | :-------------: | ------- |\n"
        )

        rows = []
        for proxy in valid_data[:limit]:
            rows.append(
                f"| {proxy['host']} | {proxy['latency_ms']} | [Connect]({proxy['url']}) |"
            )

        table = table_header + "\n".join(rows) + "\n"
        self._sections.append(table)
        return self
    
    
    def build(self) -> str:
        return "\n".join(self._sections)
    

class TelegramMessageBuilder:
    def __init__(self) -> None:
        self._lines: list[str] = []
        self._buttons: list[dict] = []

    
    def add_title(self) -> TelegramMessageBuilder:
        self._lines.append("🔄 **MTProto Proxy Update**")
        self._lines.append("")
        
        return self
    

    def add_stats(self, stats: ProxyMetrics) -> TelegramMessageBuilder:
        metrics_text = (
            f"**Pull stats:**"
            f"🟢 **Alive:** `{stats.alive_count}` of `{stats.total}`\n"
            f"⚡ **Avg. latency:** `{stats.avg_latency}` ms\n"
            f"📈 **Rate:** `{stats.rate}`"
        )

        self._lines.append(metrics_text)
        self._lines.append("")

        return self
    

    def add_top_links(self, valid_data: list[dict], limit: int = 5) -> TelegramMessageBuilder:
        if not valid_data:
            return self
        
        self._lines.append(f"🚀 **Top {limit} Fastest Proxies:**")
        for i, proxy in enumerate(valid_data[:limit], 1):
            self._lines.append(f"[Server {i}]({proxy['url']})")
        
        self._lines.append("")

        return self
    

    def add_footer(self) -> TelegramMessageBuilder:
        footer = (
            "**[GitHub](https://github.com/shablin/mtproto-proxy)** | #mtproto #proxy"
        )

        self._lines.append(footer)

        return self

    # TODO: def add_inline_buttons():

    def build(self) -> str:
        text = "\n".join(self._lines)
    
        return text