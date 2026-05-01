from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db import get_session
from app.exceptions.auth import invalid_credentials_exception
from app.schemas.auth import Token
from app.security import create_access_token, verify_password
from app.services.user_service import get_user_by_email

router = APIRouter(prefix="/token", tags=["auth"])


@router.post("", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = get_user_by_email(session, form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise invalid_credentials_exception()

    return {
        "access_token": create_access_token(data={"sub": user.email}),
        "token_type": "bearer",
    }
