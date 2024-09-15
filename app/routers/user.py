from fastapi import APIRouter

from app.config import settings
from app.crud.user import search_user_by_email
from app.dependencies import (
    ActiveUserDep,
    DBSessionDep
)
from app.schemas.response import BaseResponse
from app.schemas.user import PublicUser, ChangePasswordRequest, ResetPasswordRequest
from app.utils.auth import ph
from app.utils.gmail import send_email
from app.utils.rand import generate_random_string

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.get("/me")
async def me(user: ActiveUserDep) -> BaseResponse[PublicUser]:
    return BaseResponse(
        success=True,
        msg="ok",
        data=PublicUser(
            id=user.id,
            email=user.email,
            phone_number=user.phone_number,
            first_name=user.first_name,
            last_name=user.last_name,
            expiration_date=user.expiration_date,
            organization_id=user.organizations[0].id if user.organizations else None
        )
    )


@router.post("/reset-password")
async def reset_password(db_session: DBSessionDep, req: ResetPasswordRequest) -> BaseResponse:
    user = await search_user_by_email(db_session, req.email)
    if not user:
        return BaseResponse(
            success=True,
            msg="ок"
        )

    reset_code = generate_random_string(6)

    user.reset_password_code = reset_code

    await db_session.commit()

    await send_email(
        sender_email=settings.gmail_email,
        sender_password=settings.gmail_password,
        recipient_email=user.email,
        subject="Сброс пароля",
        message_body=f"Ваш код для сброса пароля: {reset_code}"
    )

    return BaseResponse(
        success=True,
        msg="ок"
    )


@router.post("/change-password")
async def change_password(db_session: DBSessionDep, req: ChangePasswordRequest) -> BaseResponse:
    user = await search_user_by_email(db_session, req.email)
    if not user:
        return BaseResponse(
            success=False,
            msg="неверный код"
        )

    if user.reset_password_code != req.reset_code:
        return BaseResponse(
            success=False,
            msg="неверный код"
        )

    if len(req.new_password) < 8:
        return BaseResponse(
            success=False,
            msg="пароль должен содержать не менее 8 символов"
        )

    user.password = ph.hash(req.new_password)
    user.reset_password_code = None

    await db_session.commit()

    return BaseResponse(
        success=True,
        msg="пароль успешно изменен"
    )
