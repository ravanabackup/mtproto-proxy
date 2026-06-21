import asyncio
import logging
from pathlib import Path
import urllib.request
from src import config


logger = logging.getLogger("Providers")


PROVIDERS_PATH = config.PROVIDERS_PATH
RAW_PROXY_PATH = config.RAW_PROXY_PATH


def fetch_url_sync(url: str, timeout: int = 10) -> str:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    )

    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="ignore")
    

async def download_from_provider(url: str) -> set[str]:
    try:
        logger.info("downloading from provider:", url)
        content = await asyncio.to_thread(fetch_url_sync, url)
        proxies = {
            line.strip()
            for line in content.splitlines()
            if line.strip()
        }

        logger.info(f"total extracted {len(proxies)} proxies from {url}")
        return proxies
    except Exception as e:
        logger.error("unable to download from", url, e)
        return set()


async def aggregate_proxies():
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
    
    with open(RAW_PROXY_PATH, "w", encoding="utf-8") as file:
        for proxy in sorted(all_raw_proxies):
            file.write(proxy + "\n")
    
    logger.info(f"raw proxy list successfully updated: {len(all_raw_proxies)} proxies total")