from fastapi import APIRouter
from pydantic import EmailStr
from loguru import logger

from app.dependencies import DBSessionDep
from app.exceptions import BadRequestError
from app.models.form import ContactRequest
from app.schemas.form import ContactFormRequest
from app.schemas.response import BaseResponse
from app.service.telegram import tgclient

router = APIRouter(
    prefix="/form",
    tags=["forms"],
)


@router.post("/submit-form")
async def submit_form(
    db_session: DBSessionDep,
    req: ContactFormRequest,
) -> BaseResponse:

    if not req.email and not req.phone_number:
        raise BadRequestError("Email or phone is required")

    contact_request = ContactRequest(
        name=req.name,
        email=req.email,
        phone_number=req.phone_number
    )

    db_session.add(contact_request)

    await db_session.commit()

    await db_session.refresh(contact_request)

    message = (
        f"Новая заявка:\n"
        f"ФИО: {contact_request.name}\n"
        f"Email: {contact_request.email or 'не указан'}\n"
        f"Телефон: {contact_request.phone_number or 'не указан'}"
    )

    try:
        await tgclient.send_message(message)
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения в Telegram: {e}")

    return BaseResponse(
        success=True,
        msg="ok")
