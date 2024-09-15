from typing import List

from fastapi import APIRouter

from app.dependencies import (
    ActiveUserDep,
)
from app.schemas.organization import OrganizationSuggestion, ExternalOrganization
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


@router.get("/search")
async def search_organization(_: ActiveUserDep, tax_number: str) -> BaseResponse[ExternalOrganization]:
    org = await dadata.search_organization(tax_number)
    return BaseResponse(
        success=True,
        msg="ок",
        data=org
    )


@router.get("/{organization_id}")
async def get_organization_by_id(active_user: ActiveUserDep, organization_id: int):
    pass


@router.post("/create")
async def create_organization(active_user: ActiveUserDep):
    pass
