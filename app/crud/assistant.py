from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.assistant import Assistant


async def get_all_assistants(db_session: AsyncSession) -> Sequence[Assistant]:
    rs = await db_session.execute(select(Assistant))
    return rs.scalars().all()
