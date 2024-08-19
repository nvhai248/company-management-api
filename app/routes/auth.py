from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from services import auth
from shared.database import get_db_context

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db_context),
):
    user = auth.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise auth.token_exception("Username or Password is incorrect")

    return {
        "access_token": auth.create_access_token(user, timedelta(minutes=10)),
        "token_type": "bearer",
    }
