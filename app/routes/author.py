from datetime import datetime
from uuid import UUID
from fastapi import Depends, HTTPException, APIRouter
from starlette import status
from shared.database import get_db_context
from schemas.author import Author
from models.author import AuthorModel, AuthorViewModel
from sqlalchemy.orm import Session

router = APIRouter(prefix="/authors", tags=["Author"])


def http_exception():
    return HTTPException(status_code=404, detail="Item not found")


@router.get("/")
async def get_authors(
    db: Session = Depends(get_db_context), status_code=status.HTTP_200_OK
) -> list[AuthorViewModel]:
    authors = db.query(Author).all()
    if not authors:
        raise HTTPException(status_code=404, detail="No authors found")

    return authors


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_author(
    request: AuthorModel, db: Session = Depends(get_db_context)
) -> None:
    author = Author(**request.dict())
    db.add(author)
    db.commit()


@router.put("/{author_id}", status_code=status.HTTP_200_OK)
async def create_author(
    request: AuthorModel, author_id: UUID, db: Session = Depends(get_db_context)
) -> AuthorViewModel:
    author = db.query(Author).filter(Author.id == author_id).first()
    if author is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Author Not Found"
        )

    author.full_name = request.full_name
    author.gender = request.gender
    author.updated_at = datetime.utcnow()
    db.add(author)
    db.commit()
    return author
