from typing import List

from fastapi import APIRouter

from app.dependencies import ActiveUserDep
from app.schemas.chat import CreateChatRequest, PublicAssistant, PublicChat
from app.schemas.response import BaseResponse

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
async def list_chats(user: ActiveUserDep) -> BaseResponse[List[PublicChat]]:
    pass


@router.get("/assistant/list")
async def list_assistants(user: ActiveUserDep) -> BaseResponse[List[PublicAssistant]]:
    pass
