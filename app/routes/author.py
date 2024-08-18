from fastapi import Depends, HTTPException, APIRouter
from starlette import status
from schemas.author import Author
from database import LocalSession
from models.author import AuthorModel, AuthorViewModel
from sqlalchemy.orm import Session

router = APIRouter(prefix="/authors", tags=["Author"])


def get_db_context():
    try:
        db = LocalSession()
        yield db
    finally:
        db.close()


def http_exception():
    return HTTPException(status_code=404, detail="Item not found")


@router.get("/")
async def get_authors(
    db: Session = Depends(get_db_context), status_code=status.HTTP_200_OK
) -> list[AuthorViewModel]:
    authors = db.query(Author).all()
    if not authors:
        raise HTTPException(status_code=404, detail="No authors found")
    return [
        AuthorViewModel(
            id=author.id,
            full_name=author.full_name,
            gender=author.gender.value,
            created_at=author.created_at,
        )
        for author in authors
    ]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_author(
    request: AuthorModel, db: Session = Depends(get_db_context)
) -> None:
    author = Author(**request.dict())
    db.add(author)
    db.commit()
