from datetime import datetime, UTC
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.refresh_session import RefreshSession


async def get_active_sessions_by_user_id(db_session: AsyncSession, user_id: int) -> Sequence[RefreshSession]:
    rs = await db_session.execute(
        select(RefreshSession).where(RefreshSession.user_id == user_id, RefreshSession.expires_in > datetime.now(UTC))
    )
    return rs.scalars().all()


async def get_session_by_refresh_token(db_session: AsyncSession, refresh_token: str) -> RefreshSession:
    rs = await db_session.execute(
        select(RefreshSession).where(RefreshSession.refresh_token == refresh_token)
    )
    return rs.scalars().first()
