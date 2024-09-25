import asyncio

import httpx

from app.config import settings


async def send_telegram_message(text: str):
    url = f'https://api.telegram.org/bot{settings.TELEGRAM_API_KEY}/sendMessage'
    payload = {
        'chat_id': settings.CHAT_ID,
        'text': text,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        if response.status_code != 200:
            print(f"Response: {response.text}")
            raise Exception(f"Ошибка отправки сообщения: {response.status_code} - {response.text}")

# async def main():
#     await send_telegram_message("Test message from the bot!")
#
# if __name__ == "__main__":
#     asyncio.run(main())
