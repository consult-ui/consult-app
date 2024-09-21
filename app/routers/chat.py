from typing import List

from fastapi import APIRouter

import app.crud.chat as crud
import app.service.chat as service
from app.dependencies import ActiveUserDep, DBSessionDep, OrganizationIdDep
from app.schemas.chat import CreateChatRequest, PublicAssistant, PublicChat
from app.schemas.response import BaseResponse
from app.utils.chat import make_public_chats

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@router.post("/create")
async def create_chat(user: ActiveUserDep, req: CreateChatRequest) -> BaseResponse[PublicChat]:
    pass


@router.post("/{chat_id}/delete")
async def delete_chat(user: ActiveUserDep, chat_id: int) -> BaseResponse:
    pass


@router.get("/list")
async def list_chats(
        db_session: DBSessionDep,
        user: ActiveUserDep,
        org_id: OrganizationIdDep,
) -> BaseResponse[List[PublicChat]]:
    chats = await crud.get_user_organization_chats(db_session, user.id, org_id)
    if len(chats) == 0:
        chat = await service.create_default_chat(db_session, user, org_id)
        chats = [chat]

    return BaseResponse(
        success=True,
        msg="ок",
        data=make_public_chats(chats),
    )


@router.get("/assistant/list")
async def list_assistants(user: ActiveUserDep) -> BaseResponse[List[PublicAssistant]]:
    pass
