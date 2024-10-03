import asyncio
from enum import Enum
from typing import Any

from openai import AsyncOpenAI, AsyncAssistantEventHandler
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import override

from app.config import settings
from app.models.file import File
from app.models.message import Message, MessageRole

openai_client = AsyncOpenAI(api_key=settings.openai_api_key)


class EventType(str, Enum):
    TEXT_DONE = "text_done"
    TEXT_DELTA = "text_delta"
    TEXT_CREATED = "text_created"
    MESSAGE_DONE = "message_done"


class Event(BaseModel):
    type: EventType
    payload: Any


class EventHandler(AsyncAssistantEventHandler):
    def __init__(self, db_session: AsyncSession, chat_id: int):
        super().__init__()
        self.db_session = db_session
        self.chat_id = chat_id
        self._event_queue = asyncio.Queue()
        self._stream_closed = False

    @override
    async def on_text_delta(self, delta, snapshot):
        await self._event_queue.put(Event(type=EventType.TEXT_DELTA, payload=delta))

    @override
    async def on_message_done(self, message) -> None:
        await self._event_queue.put(Event(type=EventType.MESSAGE_DONE, payload=message))

        msg = Message(
            chat_id=self.chat_id,
            role=MessageRole.ASSISTANT,
            openai_id=message.id,
            openai_message=message.model_dump(),
        )
        self.db_session.add(msg)

        file_ids = [a.file_id for a in message.attachments if a.file_id]
        openai_files = await asyncio.gather(
            *[openai_client.files.retrieve(file_id=i) for i in file_ids]
        )

        for f in openai_files:
            if not f:
                continue

            file = File(
                name=f.filename,
                size=f.bytes,
                chat_id=self.chat_id,
                openai_id=f.id,
            )
            self.db_session.add(file)

    @override
    async def on_end(self) -> None:
        await self.db_session.commit()
        self._stream_closed = True
        await self._event_queue.put(None)

    async def event_generator(self):
        while not self._stream_closed:
            event = await self._event_queue.get()
            if event is None:
                break

            raw = event.payload.model_dump_json()
            yield f"event: {event.type.value}\ndata: {raw}\n\n"


async def main() -> None:
    assistant = await openai_client.beta.assistants.create(
        model="gpt-4o",
        tools=[{"type": "file_search"}, {"type": "code_interpreter"}],
        name="Бизнес ассистент",
        description="Стандартный чат для общих вопросов",
        instructions="""
Представь что ты юрист и помогаешь с правовыми вопросами в сфере бизнеса. Опирайся на законы Российской федерации. В ответе всегда ссылайся на конкретные статьи из кодексов и указывай источник. 
Organization Context:
Organization Name: ПАО СБЕРБАНК
Activity Type: Денежное посредничество прочее
Tax Number: 7707083893
Head of Organization: Греф Герман Оскарович
Address: г Москва, ул Вавилова, д 19
Quarterly Income: 0
Quarterly Expenses: 0
Number of Employees: 0
Average Receipt: 0
""",
    )

    file = await openai_client.files.create(file=open("main.json", "rb"), purpose="assistants")

    thread = await openai_client.beta.threads.create()

    await openai_client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        attachments=[{"file_id": file.id, "tools": [{"type": "code_interpreter"}, {"type": "file_search"}]}],
        content="Сконвертируй этот файл в xlsx"
    )

    async with openai_client.beta.threads.runs.stream(thread_id=thread.id, assistant_id=assistant.id) as stream:
        await stream.until_done()

    messages_cursor = openai_client.beta.threads.messages.list(thread_id=thread.id)

    messages = [message async for message in messages_cursor]

    with open("resp.json", "w") as f:
        f.write("[")
        for message in messages:
            raw = message.model_dump_json()
            f.write(raw)
            f.write(",\n")
        f.write("]")


if __name__ == "__main__":
    asyncio.run(main())
