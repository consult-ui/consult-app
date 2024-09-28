from typing import List

import humanize
from fastapi import APIRouter, UploadFile
from loguru import logger

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
from app.schemas.file import DeleteFileRequest
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


@router.post("/{chat_id}/upload-file")
async def upload_file(
        db_session: DBSessionDep,
        user: ActiveUserDep,
        chat_id: int,
        upload: UploadFile
) -> BaseResponse[PublicFile]:
    if upload.size > MAX_FILE_SIZE:
        raise BadRequestError(
            f"файл {upload.filename} слишком большой. максимальный размер {humanize.naturalsize(MAX_FILE_SIZE)}")

    chat = await db_session.get(Chat, chat_id)
    if not chat:
        raise NotFoundError("чат не найден")

    if chat.user_id != user.id:
        raise NotFoundError("чат не найден")

    try:
        obj = await openai_client.files.create(file=(upload.filename, upload.file, upload.content_type, upload.headers),
                                               purpose="assistants")
    except Exception as e:
        logger.error(f"ошибка загрузки файла: {e}")
        raise BadRequestError(f"ошибка загрузки файла")

    file = File(
        chat_id=chat_id,
        name=upload.filename,
        openai_id=obj.id,
        size=upload.size,
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


@router.post("/{chat_id}/delete-file")
async def delete_file(
        db_session: DBSessionDep,
        user: ActiveUserDep,
        chat_id: int,
        req: DeleteFileRequest,
) -> BaseResponse:
    chat = await db_session.get(Chat, chat_id)
    if not chat:
        raise NotFoundError("чат не найден")

    if chat.user_id != user.id:
        raise NotFoundError("чат не найден")

    file = await db_session.get(File, req.file_id)
    if not file:
        raise NotFoundError("файл не найден")

    if file.chat_id != chat_id:
        raise NotFoundError("файл не найден")

    try:
        res = await openai_client.files.delete(file_id=file.openai_id)
        if res.deleted:
            logger.info(f"файл удален: {file.openai_id}")
    except Exception as e:
        logger.error(f"ошибка удаления файла: {e}")

    await db_session.delete(file)

    await db_session.commit()

    return BaseResponse(success=True, msg="файл удален")


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
