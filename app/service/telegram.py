import httpx
from loguru import logger

from app.config import settings


class Telegram:
    def __init__(self):
        self.client = httpx.AsyncClient(
            base_url=f'https://api.telegram.org/bot{settings.telegram_api_key}',
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
        )

    async def send_message(self, text: str):
        url = '/sendMessage'
        payload = {
            'chat_id': settings.telegram_chat_id,
            'text': text,
        }
        response = await self.client.post(url, json=payload)
        if response.status_code != 200:
            logger.error(f"ошибка отправки сообщения: {response.status_code} - {response.text}")


tgclient = Telegram()
