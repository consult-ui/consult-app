from typing import List

from fastapi import APIRouter

import app.service.chat as service
from app.crud.assistant import get_all_assistants
from app.crud.chat import get_user_organization_chats
from app.dependencies import ActiveUserDep, DBSessionDep, OrganizationIdDep
from app.exceptions import NotFoundError
from app.models.chat import Chat
from app.schemas.assistant import PublicAssistant
from app.schemas.chat import CreateChatRequest, UpdateChatRequest, PublicChat
from app.schemas.response import BaseResponse
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
        chat = await service.create_chat(db_session, user, req.assistant_id, org_id)

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

    return BaseResponse(success=True, msg="чат удален")


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
