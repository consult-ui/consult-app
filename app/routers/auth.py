from datetime import datetime, timedelta, UTC

from fastapi import APIRouter

import app.crud.refresh_session as auth_crud
import app.crud.user as user_crud
from app.dependencies import (
    DBSessionDep,
)
from app.exceptions import UnauthorizedError
from app.models.refresh_session import RefreshSession
from app.schemas.auth import RefreshTokenRequest
from app.schemas.auth import SignInRequest, TokenPair, SignOutRequest
from app.schemas.response import BaseResponse
from app.utils.auth import create_access_token, ph, JWT_EXPIRATION_DELTA

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/sign-in")
async def sign_in(db_session: DBSessionDep, req: SignInRequest) -> BaseResponse[TokenPair]:
    user = await user_crud.search_user_by_login(db_session, req.login)
    if user is None:
        raise UnauthorizedError("Неверный логин или пароль")
    try:
        ph.verify(user.password, req.password)
    except Exception as e:
        raise UnauthorizedError("Неверный логин или пароль")

    active_sessions = await auth_crud.get_active_sessions_by_user_id(db_session, user.id)
    if len(active_sessions) >= 5:
        for session in active_sessions:
            await db_session.delete(session)

    rs = RefreshSession(
        user_id=user.id,
        expires_in=datetime.now(UTC) + timedelta(days=60),
    )

    db_session.add(rs)

    await db_session.commit()

    await db_session.refresh(rs)

    access_token = create_access_token(
        data={"id": user.id}, expires_delta=JWT_EXPIRATION_DELTA
    )

    return BaseResponse(
        success=True,
        msg="ok",
        data=TokenPair(access_token=access_token, refresh_token=str(rs.refresh_token), token_type="bearer")
    )


@router.post("/sign-out")
async def sign_out(db_session: DBSessionDep, req: SignOutRequest) -> BaseResponse:
    sess = await auth_crud.get_session_by_refresh_token(db_session, req.refresh_token)
    if sess:
        await db_session.delete(sess)
        await db_session.commit()

    return BaseResponse(success=True, msg="ок")


@router.post("/refresh")
async def refresh(db_session: DBSessionDep, req: RefreshTokenRequest) -> BaseResponse[TokenPair]:
    rs = await auth_crud.get_session_by_refresh_token(db_session, req.refresh_token)
    if not rs:
        raise UnauthorizedError("Неверный токен")

    await db_session.delete(rs)

    if rs.expires_in < datetime.now(UTC):
        raise UnauthorizedError("Токен просрочен")

    rs = RefreshSession(
        user_id=rs.user_id,
        expires_in=datetime.now(UTC) + timedelta(days=60),
    )

    db_session.add(rs)

    await db_session.commit()

    await db_session.refresh(rs)

    access_token = create_access_token(
        data={"id": rs.user_id}, expires_delta=JWT_EXPIRATION_DELTA
    )

    return BaseResponse(
        success=True,
        msg="ok",
        data=TokenPair(access_token=access_token, refresh_token=str(rs.refresh_token), token_type="bearer")
    )
