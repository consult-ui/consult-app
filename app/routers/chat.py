from typing import List
from venv import logger

import humanize
from fastapi import APIRouter, UploadFile

import app.service.chat as service
from app.config import MAX_FILE_SIZE
from app.crud.assistant import get_all_assistants
from app.crud.chat import get_user_organization_chats
from app.dependencies import ActiveUserDep, DBSessionDep, OrganizationIdDep
from app.exceptions import BadRequestError
from app.exceptions import NotFoundError
from app.models.chat import Chat
from app.models.file import File
from app.schemas.assistant import PublicAssistant
from app.schemas.chat import CreateChatRequest, UpdateChatRequest, PublicChat
from app.schemas.file import PublicFile
from app.schemas.response import BaseResponse
from app.service.openai import openai_client
from app.utils.assistant import make_public_assistants
from app.utils.chat import make_public_chats, make_public_chat

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@router.post("/create")
async def create_chat(
        db_session: DBSessionDep,
        user: ActiveUserDep,
        req: CreateChatRequest,
        org_id: OrganizationIdDep,
) -> BaseResponse[PublicChat]:
    if not req.assistant_id:
        chat = await service.create_default_chat(db_session, user, org_id)
    else:
        chat = await service.create_chat(db_session, user, org_id, req.assistant_id)

    return BaseResponse(
        success=True,
        msg="чат создан",
        data=make_public_chat(chat),
    )


@router.post("/{chat_id}/update")
async def update_chat(
        db_session: DBSessionDep,
        user: ActiveUserDep,
        chat_id: int,
        req: UpdateChatRequest,
) -> BaseResponse[PublicChat]:
    chat = await db_session.get(Chat, chat_id)
    if not chat:
        raise NotFoundError("чат не найден")

    if chat.user_id != user.id:
        raise NotFoundError("чат не найден")

    if req.name:
        chat.name = req.name
    if req.color:
        chat.color = req.color

    await db_session.commit()

    return BaseResponse(
        success=True,
        msg="чат обновлен",
        data=make_public_chat(chat),
    )


@router.post("/{chat_id}/delete")
async def delete_chat(
        db_session: DBSessionDep,
        user: ActiveUserDep,
        chat_id: int,
) -> BaseResponse:
    chat = await db_session.get(Chat, chat_id)
    if not chat:
        raise NotFoundError("чат не найден")

    if chat.user_id != user.id:
        raise NotFoundError("чат не найден")

    await db_session.delete(chat)

    await db_session.commit()

    return BaseResponse(success=True, msg="чат удален")


@router.post("/{chat_id}/upload")
async def upload_file(
        db_session: DBSessionDep,
        user: ActiveUserDep,
        chat_id: int,
        file: UploadFile
) -> BaseResponse[PublicFile]:
    if file.size > MAX_FILE_SIZE:
        raise BadRequestError(
            f"файл {file.filename} слишком большой. Максимальный размер {humanize.naturalsize(MAX_FILE_SIZE)}")

    chat = await db_session.get(Chat, chat_id)
    if not chat:
        raise NotFoundError("чат не найден")

    if chat.user_id != user.id:
        raise NotFoundError("чат не найден")

    try:
        obj = await openai_client.files.create(file=(file.filename, file.file, file.content_type, file.headers),
                                               purpose="assistants")
    except Exception as e:
        logger.error(f"ошибка загрузки файла: {e}")
        raise BadRequestError(f"ошибка загрузки файла")

    file = File(
        chat_id=chat_id,
        name=file.filename,
        openai_id=obj.id,
        size=file.size,
    )

    db_session.add(file)

    await db_session.commit()
    await db_session.refresh(file)

    return BaseResponse(
        success=True,
        msg="файл загружен",
        data=PublicFile(
            id=file.id,
            name=file.name,
            size=file.size,
            created_at=file.created_at
        ),
    )


@router.get("/list")
async def list_chats(
        db_session: DBSessionDep,
        user: ActiveUserDep,
        org_id: OrganizationIdDep,
) -> BaseResponse[List[PublicChat]]:
    chats = await get_user_organization_chats(db_session, user.id, org_id)
    if not chats:
        chat = await service.create_default_chat(db_session, user, org_id)
        chats = [chat]

    return BaseResponse(
        success=True,
        msg="ок",
        data=make_public_chats(chats),
    )


@router.get("/assistant/list")
async def list_assistants(db_session: DBSessionDep, _: ActiveUserDep) -> BaseResponse[List[PublicAssistant]]:
    assistants = await get_all_assistants(db_session)
    return BaseResponse(
        success=True,
        msg="ок",
        data=make_public_assistants(assistants),
    )
