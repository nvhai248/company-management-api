from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from shared.type import PaginationResponse
from schemas.company import Company
from shared.settings import USER_DEFAULT_PASSWORD
from shared.exceptions import (
    badrequest_exception,
    forbidden_exception,
    notfound_exception,
)
from shared.database import get_db_context
from schemas.user import User, get_password_hash
from models.user import UserModel, UserViewModel
from services import auth
import math

router = APIRouter(prefix="/users", tags=["User"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    request: UserModel,
    db: Session = Depends(get_db_context),
) -> None:
    # Check if the username or email already exists
    existing_user = (
        db.query(User)
        .filter((User.username == request.username) | (User.email == request.email))
        .first()
    )

    if existing_user:
        raise badrequest_exception("Username or email already exists")

    existing_company = (
        db.query(Company).filter(Company.id == request.company_id).first()
    )

    if not existing_company:
        raise notfound_exception("Company not found")

    # Hash the password
    hashed_password = get_password_hash(USER_DEFAULT_PASSWORD)

    # Create a new user, ensuring hashed_password is set
    new_user_data = request.dict()
    new_user_data["hashed_password"] = hashed_password
    new_user = User(**new_user_data)

    db.add(new_user)
    db.commit()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_users(
    db: Session = Depends(get_db_context),
    pageNumber: int = Query(1, description="Page number"),
    pageSize: int = Query(10, description="Number of users to return per page"),
    current_user: User = Depends(auth.is_admin),
    status_code=status.HTTP_200_OK,
) -> PaginationResponse[UserViewModel]:
    total_users = db.query(User).count()

    totalPages = math.ceil(total_users / pageSize)

    offset = (pageNumber - 1) * pageSize

    # Get users for the current page
    users = db.query(User).offset(offset).limit(pageSize).all()

    # Convert users to the desired view model format
    users_data = [UserViewModel.from_orm(user) for user in users]

    return {
        "pageNumber": pageNumber,
        "totalPages": totalPages,
        "pageSize": pageSize,
        "data": users_data,
    }


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(
    user_id: str,
    current_user: User = Depends(auth.is_admin),
    db: Session = Depends(get_db_context),
) -> UserViewModel:
    # Retrieve the user by ID
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise notfound_exception("User")

    # Convert to view model and return
    return UserViewModel.from_orm(user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    current_user: User = Depends(auth.is_admin),
    db: Session = Depends(get_db_context),
) -> None:
    # Retrieve the user by ID
    user_to_delete = db.query(User).filter(User.id == user_id).first()

    if not user_to_delete:
        notfound_exception("User")

    # Prevent deleting the admin user or the current user
    if user_to_delete.is_admin:
        raise forbidden_exception("Cannot delete the admin user")

    # Delete the user
    db.delete(user_to_delete)
    db.commit()
