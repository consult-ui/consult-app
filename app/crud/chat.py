from typing import Sequence, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chat import Chat


async def get_user_organization_chats(db_session: AsyncSession, user_id: int, org_id: Optional[int]) -> Sequence[Chat]:
    rs = await db_session.execute(
        select(Chat).where(Chat.user_id == user_id, Chat.organization_id == org_id)
    )
    return rs.scalars().all()
