from datetime import datetime, timedelta, UTC

from fastapi import APIRouter

import app.crud.refresh_session as auth_crud
import app.crud.user as user_crud
from app.dependencies import (
    DBSessionDep,
)
from app.exceptions import UnauthorizedError
from app.models.refresh_session import RefreshSession
from app.schemas.auth import LoginRequest, TokenPair
from app.schemas.auth import RefreshTokenRequest
from app.utils.auth import create_access_token, ph, JWT_EXPIRATION_DELTA

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/sign-in")
async def sign_in(db_session: DBSessionDep, req: LoginRequest):
    user = await user_crud.search_user_by_login(db_session, req.login)
    if user is None or not ph.verify(user.password, req.password):
        raise UnauthorizedError("Неверный логин или пароль")

    active_sessions = await auth_crud.get_active_sessions_by_user_id(db_session, user.id)
    if len(active_sessions) >= 5:
        for session in active_sessions:
            await db_session.delete(session)

    refresh_session = RefreshSession(
        user_id=user.id,
        expires_in=datetime.now(UTC) + timedelta(days=60),
    )

    db_session.add(refresh_session)

    await db_session.commit()

    await db_session.refresh(refresh_session)

    access_token = create_access_token(
        data={"id": user.id}, expires_delta=JWT_EXPIRATION_DELTA
    )

    return TokenPair(access_token=access_token, refresh_token=refresh_session.refresh_token, token_type="bearer")


@router.post("/refresh")
async def refresh(db_session: DBSessionDep, req: RefreshTokenRequest):
    refresh_session = await auth_crud.get_session_by_refresh_token(db_session, req.refresh_token)
    if refresh_session is None:
        raise UnauthorizedError("Неверный токен")

    await db_session.delete(refresh_session)

    if refresh_session.expires_in < datetime.now(UTC):
        raise UnauthorizedError("Токен просрочен")

    refresh_session = RefreshSession(
        user_id=refresh_session.user_id,
        expires_in=datetime.now(UTC) + timedelta(days=60),
    )

    db_session.add(refresh_session)

    await db_session.commit()

    await db_session.refresh(refresh_session)

    access_token = create_access_token(
        data={"id": refresh_session.user_id}, expires_delta=JWT_EXPIRATION_DELTA
    )

    return TokenPair(access_token=access_token, refresh_token=refresh_session.refresh_token, token_type="bearer")
