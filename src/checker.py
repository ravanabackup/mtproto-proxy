import os
import asyncio
import json
import time

from urllib.parse import urlparse, parse_qs
from models import ProxyInfo


PROBE_TIMEOUT = 2
CONCURRENCY = 100

current_dir = os.path.dirname(os.path.abspath(__file__))


def parse_proxy(url: str) -> tuple[str, int, str]:
    query = parse_qs(urlparse(url).query)
    return (
        query["server"][0],
        int(query["port"][0]),
        query["secret"][0]
    )


async def probe(proxy_url: str) -> ProxyInfo:
    host, port, secret = parse_proxy(proxy_url)
    start = time.perf_counter()

    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port),
            timeout=PROBE_TIMEOUT,
        )

        latency = (time.perf_counter() - start) * 1000

        writer.close()
        await writer.wait_closed()

        return ProxyInfo(
            url=proxy_url,
            host=host,
            port=port,
            secret=secret,
            alive=True,
            latency_ms=round(latency, 2),
        )
    except Exception:
        return ProxyInfo(
            url=proxy_url,
            host=host,
            port=port,
            secret=secret,
            alive=False,
            latency_ms=None,
        )


async def bounded_probe(
        semaphore: asyncio.Semaphore,
        proxy_url: str,
):
    async with semaphore:
        return await probe(proxy_url)


async def main():
    with open(os.path.join(current_dir, "..", "raw_proxy.txt"), encoding="utf-8") as file:
        proxies = set(
            line.strip()
            for line in file
            if line.strip()
        )

    semaphore = asyncio.Semaphore(CONCURRENCY)
    
    tasks = [
        bounded_probe(semaphore, proxy)
        for proxy in proxies
    ]

    results = await asyncio.gather(*tasks)

    alive = [
        proxy
        for proxy in results
        if proxy.alive
    ]

    alive.sort(key=lambda x: x.latency_ms)

    output_json = [
        {
            "url": p.url,
            "host": p.host,
            "port": p.port,
            "secret": p.secret,
            "latency_ms": p.latency_ms,
        }
        for p in alive
    ]

    with open(os.path.join(current_dir, "..", "valid_proxy.json"), "w", encoding="utf-8") as file:
        json.dump(output_json, file, indent=2, ensure_ascii=False)
    
    with open(os.path.join(current_dir, "..", "valid_proxy.txt"), "w", encoding="utf-8") as file:
        for p in alive:
            file.write(p.url + "\n")


if __name__ == "__main__":
    asyncio.run(main=main())