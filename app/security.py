from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from app.config import settings
from app.db import get_session
from app.exceptions.auth import invalid_token_exception

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: int | None = None) -> str:
    to_encode = data.copy()

    expire_minutes = (
        expires_delta
        if expires_delta is not None
        else settings.access_token_expire_minutes
    )
    expire = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)

    if not settings.secret_key:
        raise ValueError("JWT secret key is not configured")

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):
    from app.services.user_service import get_user_by_email  # noqa: PLC0415

    try:
        if not settings.secret_key:
            raise invalid_token_exception()

        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
            options={"require": ["exp", "sub"]},
        )
        user_email = payload.get("sub")
        if not isinstance(user_email, str) or not user_email:
            raise invalid_token_exception()
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, jwt.DecodeError):
        raise invalid_token_exception()

    user = get_user_by_email(session, email=user_email)
    if not user:
        raise invalid_token_exception()
    return user
