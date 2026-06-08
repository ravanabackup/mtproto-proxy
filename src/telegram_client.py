import json
from typing import Any
import requests
from requests.exceptions import RequestException
import logging


logger = logging.getLogger("Telegram")
logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s [%(levelname)s]"
        "[%(name)s]: %(message)s"
    )
)


class TelegramClient:
    def __init__(self, token: str, timeout: int = 10) -> None:
        if not token:
            raise ValueError("Telegram bot token is not provided")
        
        self._token = token
        self.timeout = timeout
        self._base_telegram_api_url = "https://api.telegram.org"
        self._base_url = f"{self._base_telegram_api_url}/bot{self._token}"

        self._session = requests.Session()
        self._session.headers.update({
            "Content-Type": "application/json"
        })

    
    def send_message(
            self,
            chat_id: list[int | str],
            text: str,
            parse_mode: str = "Markdown",
            disable_web_page_preview: bool = True,
    ) -> bool:
        url = f"{self._base_url}/sendMessage"

        payload = {
            "text": text,
            "parse_mode": parse_mode,
            "disable_web_page_preview": disable_web_page_preview
        }

        try:
            logger.info(f"message will be sent to: {chat_id}")

            for cid in chat_id:
                logger.info(f"sending message... (cid: {cid})")

                payload["chat_id"] = cid

                response = self._session.post(url=url, json=payload, timeout=self.timeout)
                response_data = response.json()

                if response.status_code == 200 and response_data.get("ok"):
                    logger.info(f"message sent to {chat_id}")

                    return True
            
                logger.error(f"telegram says: {response.status_code}")
                error_details = json.dumps(response_data, indent=2, ensure_ascii=False)
                logger.error(f"telegram error details: {error_details}")

                return False
        except RequestException as e:
            logger.error(f"network error (cid: {chat_id}): {e}")

            return False
        

    def close(self):
        self._session.close()