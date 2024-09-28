from openai import AsyncOpenAI

from app.config import settings

openai_client = AsyncOpenAI(api_key=settings.openai_api_key)

openai_client.beta.assistants.create()

openai_client.beta.assistants.retrieve()
