from fastapi import APIRouter

from app.dependencies import (
    ActiveUserDep,
)
from app.schemas.response import BaseResponse
from app.schemas.user import PublicUser

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.get("/me")
async def me(user: ActiveUserDep) -> BaseResponse[PublicUser]:
    return BaseResponse(
        success=True,
        msg="ok",
        data=PublicUser(
            id=user.id,
            email=user.email,
            phone_number=user.phone_number,
            first_name=user.first_name,
            last_name=user.last_name,
            expiration_date=user.expiration_date,
        )
    )
