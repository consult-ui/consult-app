import random

from fastapi import APIRouter

from app.crud.chat import get_user_organization_chats
from app.dependencies import ActiveUserDep, DBSessionDep, OrganizationIdDep
from app.prompts.default import daily_tip
from app.schemas.response import BaseResponse
from app.service.openai_api import openai_client

router = APIRouter(
    prefix="/etc",
    tags=["etc"],
)


@router.get("/tip")
async def daily_tip(
        db_session: DBSessionDep,
        user: ActiveUserDep,
        org_id: OrganizationIdDep,
) -> BaseResponse[str]:
    chats = await get_user_organization_chats(db_session, user.id, org_id)

    chat = random.choice(chats)

    completion = await openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": chat.system_prompt
            },
            {
                "role": "user",
                "content": daily_tip
            }
        ],
        temperature=0.9,
    )

    return BaseResponse(
        success=True,
        msg="ок",
        data=completion.choices[0].message.content,
    )
