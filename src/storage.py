import json
import logging
from src import config


logger = logging.getLogger("Storage")


def load_raw_proxies() -> set[str]:
    if not config.RAW_PROXY_PATH.exists():
        return set()
    with open(config.RAW_PROXY_PATH, "r", encoding="utf-8") as file:
        logger.info("loaded raw proxy list")
        return {line.strip() for line in file if line.strip()}


def load_valid_json() -> list[dict]:
    if not config.VALID_PROXY_JSON_PATH.exists():
        return []
    with open(config.VALID_PROXY_JSON_PATH, "r", encoding="utf-8") as file:
        logger.info("loaded valid proxy list (JSON)")
        return json.load(file)
    

def save_results(alive_proxies: list):
    config.DATA_DIR.mkdir(exist_ok=True)

    output_json = [
        {
            "url": p.url,
            "host": p.host,
            "port": p.port,
            "secret": p.secret,
            "latency_ms": p.latency_ms,
        }
        for p in alive_proxies
    ]

    with open(config.VALID_PROXY_JSON_PATH, "w", encoding="utf-8") as file:
        json.dump(output_json, file, indent=2, ensure_ascii=False)
        logger.info("saved valid proxy list (JSON)")

    with open(config.VALID_PROXY_TXT_PATH, "w", encoding="utf-8") as file:
        for p in alive_proxies:
            file.write(p.url + "\n")
            
        logger.info("saved valid proxy list (TXT)")