import logging
import os
from pathlib import Path


logger = logging.getLogger("Config")


BASE_DIR = Path(__file__).resolve().parent.parent


DATA_DIR = BASE_DIR / "data"
RAW_PROXY_PATH = DATA_DIR / "raw_proxy.txt"
VALID_PROXY_JSON_PATH = DATA_DIR / "valid_proxy.json"
VALID_PROXY_TXT_PATH = DATA_DIR / "valid_proxy.txt"
README_PATH = BASE_DIR / "README.md"


PROBE_TIMEOUT = 5.0
CONCURRENCY = 100


TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_BOT_OWNER_ID = os.environ.get("TELEGRAM_BOT_OWNER_ID")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")


try:
    TELEGRAM_CHAT_ID = [
        chat.strip()
        for chat in TELEGRAM_CHAT_ID.split(',')
        if chat.strip()
    ]
except Exception:
    raise Exception


if not TELEGRAM_BOT_TOKEN:
    logger.warning("env TELEGRAM_BOT_TOKEN not found")
elif not TELEGRAM_BOT_OWNER_ID:
    logger.warning("env TELEGRAM_BOT_OWNER_ID not found")
elif not TELEGRAM_CHAT_ID:
    logger.warning("env TELEGRAM_CHAT_ID not found")