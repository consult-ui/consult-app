from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.message import Message


async def get_chat_messages(db_session: AsyncSession, chat_id: int) -> Sequence[Message]:
    rs = await db_session.execute(
        select(Message).where(Message.chat_id == chat_id)
    )
    return rs.scalars().all()
