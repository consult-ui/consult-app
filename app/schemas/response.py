from pydantic import BaseModel
from typing import Generic, Optional, TypeVar, Sequence

T = TypeVar("T")


class BaseResponse(BaseModel, Generic[T]):
    success: bool
    msg: str
    data: Optional[T] = None
    errors: Optional[Sequence[dict]] = None
