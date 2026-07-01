import asyncio
import logging
from pathlib import Path
import urllib.request
from urllib.error import URLError, HTTPError
from src import config
from typing import Literal

from src.exceptions import (
    ProviderFetchError,
    ProviderParseError,
)


logger = logging.getLogger("Providers")


PROVIDERS_PATH = config.PROVIDERS_PATH
RAW_PROXY_PATH = config.RAW_PROXY_PATH


def write_raw_proxies(
        entries: set[str],
        mode: Literal["overwrite", "append"]
) -> None:
    file_mode = "w" if mode == "overwrite" else "a"
    with open(RAW_PROXY_PATH, file_mode, encoding="utf-8") as file:
        for proxy in sorted(entries):
            file.write(proxy + "\n")
    
    logger.info(
        f"raw proxy list successfully updated in {mode.upper()} mode: "
        f"{len(entries)} proxies total"
    )


def fetch_url_sync(url: str, timeout: int = 10) -> str:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.read().decode("utf-8", errors="ignore")
    except HTTPError as e:
        raise ProviderFetchError(url, f"HTTP {e.code}") from e
    except URLError as e:
        raise ProviderFetchError(url, f"URL error: {e.reason}") from e
    except TimeoutError as e:
        raise ProviderFetchError(url, "timeout") from e
    

async def download_from_provider(url: str) -> set[str]:
    try:
        logger.info(f"downloading from provider: {url}")
        content = await asyncio.to_thread(fetch_url_sync, url)
    except ProviderFetchError as e:
        logger.warning(f"skipping provider {url}: {e}")
        return set()
    
    proxies = {
        line.strip()
        for line in content.splitlines()
        if line.strip() and not line.startswith("#")
    }

    if not proxies:
        raise ProviderParseError(url, "no proxies extracted")
    
    logger.info(f"total extracted {len(proxies)} proxies from {url}")
    return proxies


async def aggregate_proxies(write_mode: Literal["overwrite", "append"] = "overwrite"):
    if not PROVIDERS_PATH.exists():
        logger.warning("providers file not found!")
        return
    
    urls = []
    with open(PROVIDERS_PATH, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if line and not line.startswith("#"):
                urls.append(line)
    
    if not urls:
        logger.warning("no links found in providers file")
        return
    
    logger.info(f"total found {len(urls)} providers")

    tasks = [download_from_provider(url) for url in urls]
    results = await asyncio.gather(*tasks)

    all_raw_proxies = set()
    for proxy_set in results:
        all_raw_proxies.update(proxy_set)

    if not all_raw_proxies:
        logger.warning("no provider returned proxy links")
        return
    
    write_raw_proxies(all_raw_proxies, mode=write_mode)