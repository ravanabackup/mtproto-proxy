import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


DATA_DIR = BASE_DIR / "data"
RAW_PROXY_PATH = DATA_DIR / "raw_proxy.txt"
VALID_PROXY_JSON_PATH = DATA_DIR / "valid_proxy.json"
VALID_PROXY_TXT_PATH = DATA_DIR / "valid_proxy.txt"
README_PATH = BASE_DIR / "README.md"


PROBE_TIMEOUT = 2.0
CONCURRENCY = 100


TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")