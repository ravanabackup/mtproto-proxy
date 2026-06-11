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
    def __init__(self, token: str | Any, timeout: int = 10) -> None:
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
            chat_id: list[int | str] | Any,
            text: str,
            parse_mode: str = "Markdown",
            disable_web_page_preview: bool = True,
            reply_markup: dict[str, Any] | None = None
    ) -> bool:
        url = f"{self._base_url}/sendMessage"

        payload = {
            "text": text,
            "parse_mode": parse_mode,
            "disable_web_page_preview": disable_web_page_preview,
        }

        if reply_markup:
            payload["reply_markup"] = reply_markup

        try:
            logger.info(f"sending message... (cid: {chat_id})")

            payload["chat_id"] = chat_id

            response = self._session.post(url=url, json=payload, timeout=self.timeout)
            response_data = response.json()

            if response.status_code == 200 and response_data.get("ok"):
                logger.info(f"message sent to {chat_id}")

                return True
        
            logger.error(f"telegram says: {response.status_code} (cid: {chat_id})")
            error_details = json.dumps(response_data, indent=2, ensure_ascii=False)
            logger.error(f"telegram error details: {error_details}")

            return False
        except RequestException as e:
            logger.error(f"network error (cid: {chat_id}): {e}")

            return False


    def broadcast(
            self,
            chat_ids: list[int | str] | Any,
            text: str,
            parse_mode: str = "Markdown",
            disable_web_page_preview: bool = True,
            reply_markup: dict[str, Any] | None = None
    ):
        for cid in chat_ids:
            self.send_message(
                chat_id=cid,
                text=text,
                parse_mode=parse_mode,
                disable_web_page_preview=disable_web_page_preview,
                reply_markup=reply_markup
            )


    def close(self):
        self._session.close()