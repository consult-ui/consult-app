from typing import List

from fastapi import APIRouter

from app.dependencies import (
    ActiveUserDep,
)
from app.schemas.organization import OrganizationSuggestion
from app.schemas.response import BaseResponse
from app.service.dadata import dadata

router = APIRouter(
    prefix="/organization",
    tags=["organization"],
)


@router.get("/suggest")
async def suggest(_: ActiveUserDep, q: str) -> BaseResponse[List[OrganizationSuggestion]]:
    suggestions = await dadata.suggest_organizations(q)
    return BaseResponse(
        success=True,
        msg="ок",
        data=suggestions
    )
