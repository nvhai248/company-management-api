from typing import Generic, List, TypeVar, Any
from pydantic import BaseModel

T = TypeVar("T")


class PaginationResponse(Generic[T], BaseModel):
    pageNumber: int
    totalPages: int
    pageSize: int
    data: List[T]
