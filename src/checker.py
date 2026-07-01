import logging
import asyncio
import time

from urllib.parse import urlparse, parse_qs
from src.models import ProxyInfo
from src import config

from src.exceptions import (
    InvalidProxyURLError,
    MissingProxyFieldError,
    ProxyConnectionError,
    ProxyTimeoutError,
    ProxyCheckerError,
)


logger = logging.getLogger("ProxyChecker")


def parse_proxy(url: str) -> tuple[str, int, str]:
    try:
        parsed = urlparse(url)
        query = parse_qs(parsed.query)
    except ValueError as e:
        raise InvalidProxyURLError(url, str(e)) from e
    
    for field in ("server", "port", "secret"):
        if field not in query or not query[field]:
            raise MissingProxyFieldError(url, field)
    
    try:
        port = int(query["port"][0])
    except (ValueError, TypeError) as e:
        raise InvalidProxyURLError(url, f"port is not int: {e}") from e
    
    return query["server"][0], port, query["secret"][0]


async def probe(proxy_url: str) -> ProxyInfo:
    host, port, secret = parse_proxy(proxy_url)
    start = time.perf_counter()

    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port),
            timeout=config.PROBE_TIMEOUT,
        )
    except asyncio.TimeoutError as e:
        raise ProxyTimeoutError(host, port, config.PROBE_TIMEOUT) from e
    except OSError as e:
        raise ProxyConnectionError(host, port, str(e)) from e

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


async def bounded_probe(
        semaphore: asyncio.Semaphore,
        proxy_url: str,
) -> ProxyInfo:
    async with semaphore:
        try:
            return await probe(proxy_url)
        except ProxyCheckerError as e:
            logger.debug(f"proxy dead: {e}")
            host, port, secret = parse_proxy(proxy_url)
            
            return ProxyInfo(
                url=proxy_url,
                host=host,
                port=port,
                secret=secret,
                alive=False,
                latency_ms=None,
            )



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