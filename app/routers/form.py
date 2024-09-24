from fastapi import APIRouter
from pydantic import EmailStr

from app.dependencies import DBSessionDep
from app.exceptions import BadRequestError
from app.models.form import ContactRequest
from app.schemas.response import BaseResponse

router = APIRouter(
    prefix="/form",
    tags=["forms"],
)


@router.post("/submit_form")
async def submit_form(
    db_session: DBSessionDep,
    first_name: str,
    last_name: str,
    email: EmailStr = None,
    phone_number: str = None,
) -> BaseResponse:
    if not first_name or not last_name:
        raise BadRequestError("ФИО является обязательным полем")

    form_user = ContactRequest(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone_number=phone_number
    )

    db_session.add(form_user)

    await db_session.commit()

    await db_session.refresh(form_user)

    message = (
        f"Новая заявка:\n"
        f"ФИО: {form_user.first_name} {form_user.last_name}\n"
        f"Email: {form_user.email or 'не указан'}\n"
        f"Телефон: {form_user.phone_number or 'не указан'}"
    )

    # send_telegram_message(message)    тут надо как то телегу реализовать

    return BaseResponse(
        success=True,
        msg="ok")


