from typing import Annotated

from fastapi import Depends
from fastapi import Header
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db import get_db_session
from app.exceptions import UnauthorizedError, NotFoundError, AccessDeniedError
from app.models.user import User

import jwt

from datetime import timezone, datetime


DBSessionDep = Annotated[AsyncSession, Depends(get_db_session)]


def get_current_user_id(authorization: Annotated[str, Header()]) -> int:
    if not authorization:
        raise UnauthorizedError("unauthorized")

    parts = authorization.split(" ")
    if len(parts) != 2:
        raise UnauthorizedError("invalid authorization header")

    token = parts[1]
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[JWT_ALGORITHM])
        id = payload.get("id")
        if id is None:
            raise UnauthorizedError("invalid authorization token")
        return int(id)
    except Exception as e:
        logger.error(f"failed to parse access token: {e}")
        raise UnauthorizedError("invalid access token")


CurrentUserIdDep = Annotated[int, Depends(get_current_user_id)]


async def get_active_user(id: CurrentUserIdDep, db_session: DBSessionDep) -> User:
    user = await db_session.get(User, id)
    if user is None:
        raise NotFoundError(f"user {id} not found")

    if user.expiration_date < datetime.now(timezone.utc):
        raise AccessDeniedError("User is not active")

    return user


ActiveUserDep = Annotated[User, Depends(get_active_user)]
