import os
import json
from datetime import datetime, UTC
from models import ProxyMetrics


current_dir = os.path.dirname(os.path.abspath(__file__))
raw_proxy_path = os.path.join(current_dir, "..", "raw_proxy.txt") 
valid_proxy_path = os.path.join(current_dir, "..", "valid_proxy.json") 


with open(raw_proxy_path, "r") as raw, open(valid_proxy_path, "r") as valid:
    stats = ProxyMetrics.calculate_from_files(raw, valid)

updated = datetime.now(
    UTC
).strftime(
    "%Y-%m-%d %H:%M:%S UTC"
)

readme = f"""# MTProto Proxy 🚀🔒

> [!NOTE]
> **Last Update:** _{updated}_

This repository provides auto-updating proxies
for Telegram to help you bypass the messenger's
restrictions in Russia 🔒🇷🇺

Proxies are updated every **2 hours**, after which
tracking is conducted, which you can review below.
Additionally, below you will find a table with
the best ones and a link for instant connection

**Valid proxies are available for viewing and
downloading and are located in the files:** 📥
- 📄 [.TXT](https://github.com/shablin/mtproto-proxy/blob/main/valid_proxy.txt) (`valid_proxy.txt`)
- 📄 [.JSON](https://github.com/shablin/mtproto-proxy/blob/main/valid_proxy.json) (`valid_proxy.json`) 

> [!WARNING]
> At the moment, an imprecise method is used to measure latency.
> This will be fixed in the future.
> Also note that some proxies may be unavailable in your region


## 📊 Stats

| 🔢 Total | 🟢 Alive | 🔴 Dead | ⚡ Avg. Latency | 📈 Rate |
| :-:   | :-:   | :-:  | :-:  | :-: |
|{stats.total}|{stats.alive_count}|{stats.dead_count}|{stats.avg_latency} ms|{stats.rate}%|

##  🌐 Top 20 Fastest Proxies
| 🖥️ Host | ⚡ Latency (ms) | 🔗 Link |
|---|:---:|---|
"""

for proxy in stats.valid[:20]:
    readme += (
        f"| {proxy["host"]} "
        f"| {proxy["latency_ms"]} "
        f"| [Connect]({proxy["url"]}) |\n"
    )

with open(os.path.join(current_dir, "..", "README.md"), "w", encoding="utf-8") as file:
    file.write(readme)
