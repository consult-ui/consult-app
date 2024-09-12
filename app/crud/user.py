from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


async def search_user_by_login(db_session: AsyncSession, login: str) -> Optional[User]:
    user = await db_session.execute(
        select(User).where((User.email == login) | (User.phone_number == login))
    )
    return user.scalars().first()


async def search_user_by_email(db_session: AsyncSession, email: str) -> Optional[User]:
    user = await db_session.execute(select(User).where(User.email == email))
    return user.scalars().first()
