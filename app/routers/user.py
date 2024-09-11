from fastapi import APIRouter
from app.dependencies import (
    ActiveUserDep,
)

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.post("/me")
async def me(user: ActiveUserDep):
    return user
