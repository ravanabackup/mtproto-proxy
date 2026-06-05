import os
import json
from datetime import datetime, UTC


current_dir = os.path.dirname(os.path.abspath(__file__))


with open(os.path.join(current_dir, "..", "valid_proxy.json"), encoding="utf-8") as file:
    valid = json.load(file)

with open(os.path.join(current_dir, "..", "raw_proxy.txt"), encoding="utf-8") as file:
    total = len(
        [
            line
            for line in file
            if line.strip()
        ]
    )


alive_count = len(valid)
dead_count = total - alive_count

avg_latency = (
    round(
        sum(
            p["latency_ms"]
            for p in valid
        )
        / alive_count,
        2,
    )
    if alive_count
    else 0
)

fastest = (
    min(
        p["latency_ms"]
        for p in valid
    )
    if alive_count
    else "-"
)

slowest = (
    max(
        p["latency_ms"]
        for p in valid
    )
    if alive_count
    else "-"
)

updated = datetime.now(
    UTC
).strftime(
    "%Y-%m-%d %H:%M:%S UTC"
)

rate = round((alive_count / total * 100), 1) if total else 0

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

## 📊 Stats

| 🔢 Total | 🟢 Alive | 🔴 Dead | ⚡ Avg. Latency | 📈 Rate |
| :-:   | :-:   | :-:  | :-:  | :-: |
|{total}|{alive_count}|{dead_count}|{avg_latency} ms|{rate}%|

##  🌐 Top 20 Fastest Proxies
| 🖥️ Host | ⚡ Latency (ms) | 🔗 Link |
|---|:---:|---|
"""

for proxy in valid[:20]:
    readme += (
        f"| {proxy["host"]} "
        f"| {proxy["latency_ms"]} "
        f"| [Connect]({proxy["url"]}) |\n"
    )

with open(os.path.join(current_dir, "..", "README.md"), "w", encoding="utf-8") as file:
    file.write(readme)
