import asyncio
import pathlib
from typing import List

import humanize
from fastapi import APIRouter, UploadFile
from fastapi.responses import StreamingResponse
from loguru import logger

import app.service.chat as service
from app.config import MAX_FILE_SIZE, MAX_IMAGE_SIZE
from app.crud.assistant import get_all_assistants
from app.crud.chat import get_user_organization_chats
from app.crud.file import get_file_by_openai_id, get_files_by_openai_ids
from app.dependencies import ActiveUserDep, DBSessionDep, OrganizationIdDep
from app.exceptions import BadRequestError
from app.exceptions import NotFoundError
from app.models.chat import Chat
from app.models.file import File
from app.models.message import Message, MessageRole
from app.schemas.assistant import PublicAssistant
from app.schemas.chat import CreateChatRequest, UpdateChatRequest, PublicChat
from app.schemas.chat import SendMessageRequest
from app.schemas.file import DeleteFileRequest
from app.schemas.file import PublicFile
from app.schemas.response import BaseResponse
from app.service.openai_api import openai_client, EventHandler
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


files_search_ext = {".c", ".cpp", ".cs", ".css", ".doc", ".docx", ".go", ".html", ".java", ".js", ".json", ".md",
                    ".pdf", ".php", ".pptx", ".py", ".rb", ".sh", ".tex", ".ts", ".txt"}

code_interpreter_ext = {".c", ".cpp", ".cs", ".css", ".csv", ".doc", ".docx", ".gif", ".html", ".java", ".jpeg", ".jpg",
                        ".js", ".json", ".md", ".pdf", ".php", ".pkl", ".png", ".pptx", ".py", ".rb", ".sh", ".tar",
                        ".tex", ".ts", ".txt", ".xlsx", ".xml", ".zip"}

images_ext = {".png", ".jpeg", ".jpg", ".webp", ".gif"}


@router.post("/{chat_id}/upload-file")
async def upload_file(
        db_session: DBSessionDep,
        user: ActiveUserDep,
        chat_id: int,
        upload: UploadFile
) -> BaseResponse[PublicFile]:
    ext = pathlib.Path(upload.filename).suffix
    if ext not in code_interpreter_ext and ext not in files_search_ext and ext not in images_ext:
        raise BadRequestError(f"неподдерживаемый формат файла {ext}")

    if ext in images_ext:
        if upload.size > MAX_IMAGE_SIZE:
            raise BadRequestError(
                f"медиа файл {upload.filename} слишком большой. максимальный размер {humanize.naturalsize(MAX_IMAGE_SIZE)}")
        purpose = "vision"
    else:
        if upload.size > MAX_FILE_SIZE:
            raise BadRequestError(
                f"файл {upload.filename} слишком большой. максимальный размер {humanize.naturalsize(MAX_FILE_SIZE)}")
        purpose = "assistants"

    chat = await db_session.get(Chat, chat_id)
    if not chat:
        raise NotFoundError("чат не найден")

    if chat.user_id != user.id:
        raise NotFoundError("чат не найден")

    try:
        obj = await openai_client.files.create(file=(upload.filename, upload.file, upload.content_type, upload.headers),
                                               purpose=purpose)
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
            id=file.openai_id,
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

    file = await get_file_by_openai_id(db_session, req.file_id)
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


@router.post("/{chat_id}/send")
async def send_message(
        db_session: DBSessionDep,
        user: ActiveUserDep,
        chat_id: int,
        req: SendMessageRequest
) -> StreamingResponse:
    chat = await db_session.get(Chat, chat_id)
    if not chat:
        raise NotFoundError("чат не найден")

    if chat.user_id != user.id:
        raise NotFoundError("чат не найден")

    tools = []
    if len(req.attachments) > 0:
        files = await get_files_by_openai_ids(db_session, req.attachments)

        file_search_unsupported = False
        code_interpreter_unsupported = False
        for file in files:
            ext = pathlib.Path(file.name).suffix
            if ext not in files_search_ext:
                file_search_unsupported = True
            if ext not in code_interpreter_ext:
                code_interpreter_unsupported = True

            if file_search_unsupported and code_interpreter_unsupported:
                break

        if not file_search_unsupported:
            tools.append({"type": "file_search"})
        if not code_interpreter_unsupported:
            tools.append({"type": "code_interpreter"})

    handler = EventHandler()

    content = []
    for node in req.content:
        if node.type == "text":
            content.append({"type": "text", "text": node.text})
        elif node.type == "image_file":
            content.append({"type": "image_file", "image_file": {"file_id": node.image_file.file_id, "detail": "auto"}})

    openai_msg = await openai_client.beta.threads.messages.create(thread_id=chat.openai_thread_id,
                                                                  content=content,
                                                                  role="user")

    user_msg = Message(
        chat_id=chat_id,
        role=MessageRole.USER,
        openai_id=openai_msg.id,
        openai_msg=openai_msg,
    )

    db_session.add(user_msg)

    async def drain_steam():
        async with openai_client.beta.threads.runs.stream(thread_id=chat.openai_thread_id,
                                                          assistant_id=chat.openai_assistant_id,
                                                          event_handler=handler) as stream:
            await stream.until_done()

    asyncio.create_task(drain_steam())

    return StreamingResponse(content=handler.event_generator(), media_type="text/event-stream")


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
