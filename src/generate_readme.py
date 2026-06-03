import json
from datetime import datetime, UTC


with open("../valid_proxy.json", encoding="utf-8") as file:
    valid = json.load(file)

with open("../proxies.txt", encoding="utf-8") as file:
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

readme = f"""# MTProto Proxy


## 📊 Stats

| Total | Alive | Dead | Avg. Latency | Rate |
| :-:   | :-:   | :-:  | :-:  | :-: |
|{total}|{alive_count}|{dead_count}|{avg_latency} ms|{rate}%|

**_Last Update:_** _{updated}_

## Top 20 Fastest Proxies
| Host | Latency (ms) | Link |
|---|:---:|---|
"""

for proxy in valid[:20]:
    readme += (
        f"| {proxy["host"]} "
        f"| {proxy["latency_ms"]} "
        f"| [Connect]({proxy["url"]}) |\n"
    )

with open("../README.md", "w", encoding="utf-8") as file:
    file.write(readme)