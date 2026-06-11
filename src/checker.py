import logging
import asyncio
import time

from urllib.parse import urlparse, parse_qs
from src.models import ProxyInfo
from src import config


logger = logging.getLogger("ProxyChecker")


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
            timeout=config.PROBE_TIMEOUT,
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
) -> ProxyInfo:
    async with semaphore:
        return await probe(proxy_url)


async def run_checker(proxies: set[str]) -> list[ProxyInfo]:
    logger.info(f"testing proxy... ({len(proxies)} unique)")
    semaphore = asyncio.Semaphore(config.CONCURRENCY)
    tasks = [
        bounded_probe(semaphore, proxy)
        for proxy in proxies
    ]

    results = await asyncio.gather(*tasks)

    alive = [p for p in results if p.alive]
    alive.sort(key=lambda x: x.latency_ms)
    
    return alive