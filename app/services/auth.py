from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from shared.exceptions import forbidden_exception
from shared.settings import JWT_ALGORITHM, JWT_SECRET
from schemas.user import User, verify_password
from sqlalchemy.orm import Session
from starlette import status

oa2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")


def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()

    if not user:
        return False

    if not verify_password(password, user.hashed_password):
        return False

    return user


def create_access_token(user: User, expires: Optional[timedelta] = None):
    claims = {
        "sub": user.username,
        "id": str(user.id),
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_admin": user.is_admin,
    }

    expires = (
        datetime.utcnow() + expires
        if expires
        else datetime.utcnow() + timedelta(minutes=5)
    )

    claims.update({"exp": expires})
    return jwt.encode(claims, JWT_SECRET, algorithm=JWT_ALGORITHM)


def token_interceptor(token: str = Depends(oa2_bearer)) -> User:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("id")
        username = payload.get("sub")
        first_name = payload.get("first_name")
        last_name = payload.get("last_name")
        is_admin = payload.get("is_admin")

        if not user_id or not username:
            raise token_exception("Invalid credentials")

        return User(
            id=UUID(user_id),
            username=username,
            first_name=first_name,
            last_name=last_name,
            is_admin=is_admin,
        )
    except jwt.ExpiredSignatureError:
        raise token_exception("Expired token")
    except jwt.InvalidTokenError:
        raise token_exception("Invalid token")


def is_admin(current_user: User = Depends(token_interceptor)) -> User:
    if not current_user.is_admin:
        raise forbidden_exception()

    return current_user


def token_exception(message: str):
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=message)
