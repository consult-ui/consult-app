from typing import List

from fastapi import APIRouter

import app.crud.assistant as assistant_crud
import app.crud.chat as chat_crud
import app.service.chat as service
from app.dependencies import ActiveUserDep, DBSessionDep, OrganizationIdDep
from app.exceptions import NotFoundError
from app.models.chat import Chat
from app.schemas.assistant import PublicAssistant
from app.schemas.chat import CreateChatRequest, PublicChat
from app.schemas.response import BaseResponse
from app.utils.assistant import make_public_assistants
from app.utils.chat import make_public_chats

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@router.post("/create")
async def create_chat(user: ActiveUserDep, req: CreateChatRequest) -> BaseResponse[PublicChat]:
    pass


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
    chats = await chat_crud.get_user_organization_chats(db_session, user.id, org_id)
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
    assistants = await assistant_crud.get_all_assistants(db_session)
    return BaseResponse(
        success=True,
        msg="ок",
        data=make_public_assistants(assistants),
    )
