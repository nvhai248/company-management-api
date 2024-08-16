from fastapi import HTTPException, APIRouter
from starlette import status

from models.author import AuthorModel, AuthorViewModel

router = APIRouter(prefix="/authors", tags=["Author"])


def http_exception():
    return HTTPException(status_code=404, detail="Item not found")


@router.get("/", response_model=list(AuthorViewModel))
async def get_authors(
    status_code=status.HTTP_200_OK,
):
    return []


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AuthorViewModel)
async def create_author(author: AuthorModel):
    return author
