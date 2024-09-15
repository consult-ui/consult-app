from typing import List

from fastapi import APIRouter

from app.dependencies import (
    ActiveUserDep,
)
from app.dependencies import DBSessionDep
from app.exceptions import BadRequestError, NotFoundError
from app.models.organization import Organization
from app.schemas.organization import (
    PublicOrganization,
    ExternalOrganization,
    OrganizationSuggestion,
    CreateOrganizationRequest,
)
from app.schemas.response import BaseResponse
from app.service.dadata import dadata
from app.utils.organization import make_public_organization

router = APIRouter(
    prefix="/organization",
    tags=["organization"],
)


@router.post("/create")
async def create_organization(
        db_session: DBSessionDep,
        user: ActiveUserDep,
        req: CreateOrganizationRequest
) -> BaseResponse[PublicOrganization]:
    if user.organizations:
        raise BadRequestError("организация уже создана")

    org = Organization(
        name=req.name,
        activity_type=req.activity_type,
        tax_number=req.tax_number,
        head_name=req.head_name,
        address=req.address,
        quarterly_income=req.quarterly_income,
        quarterly_expenses=req.quarterly_expenses,
        number_employees=req.number_employees,
        average_receipt=req.average_receipt,
        context=req.context
    )

    user.organizations.append(org)

    await db_session.commit()

    return BaseResponse(
        success=True,
        msg="ок",
        data=make_public_organization(org)
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
async def get_organization_by_id(user: ActiveUserDep, organization_id: int):
    for org in user.organizations:
        if org.id == organization_id:
            return BaseResponse(
                success=True,
                msg="ок",
                data=make_public_organization(org)
            )

    raise NotFoundError("организация не найдена")
