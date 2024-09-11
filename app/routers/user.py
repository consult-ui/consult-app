from datetime import timedelta
from fastapi import APIRouter
from app.dependencies import (
    DBSessionDep,
    ActiveUserDep,
)
from app.models.auth import LoginRequest, Token
from app.models.user import User
from sqlalchemy import select
from app.exceptions import UnauthorizedError
from app.utils.auth import create_access_token, ph, JWT_EXPIRATION_DELTA

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.post("/sign-in")
async def sign_in(db_session: DBSessionDep, req: LoginRequest):
    user = await db_session.execute(
        select(User).where((User.email == req.login) | (User.phone_number == req.login))
    )

    user = user.scalars().first()

    if user is None or not ph.verify(user.password, req.password):
        raise UnauthorizedError("Неверный логин или пароль")

    access_token = create_access_token(
        data={"id": user.id}, expires_delta=JWT_EXPIRATION_DELTA
    )

    return Token(access_token=access_token, token_type="bearer")


@router.post("/me")
async def me(user: ActiveUserDep):
    return user
