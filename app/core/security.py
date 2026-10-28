from collections.abc import Generator
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, Request, status
from jwt import InvalidTokenError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.db import get_db_session
from app.repositories.member import MemberRepository, UserProfile

JWT_ISSUER = "wke-api-users"


def _jwt_secret() -> str:
    secret = settings.JWT_SECRET_KEY
    if len(secret) < 32:
        raise RuntimeError("JWT_SECRET_KEY must contain at least 32 characters")
    return secret


def create_access_token(data: dict) -> str:
    subject = data.get("sub")
    if subject is None or not str(subject).isdigit() or int(subject) < 1:
        raise ValueError("JWT subject must be a positive user ID")
    if settings.ACCESS_TOKEN_EXPIRE_SECONDS <= 0:
        raise RuntimeError("ACCESS_TOKEN_EXPIRE_SECONDS must be positive")

    now = datetime.now(timezone.utc)
    payload = {
        **data,
        "sub": str(subject),
        "iss": JWT_ISSUER,
        "iat": now,
        "exp": now + timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS),
    }
    return jwt.encode(payload, _jwt_secret(), algorithm="HS256")


def _get_user_id(request: Request) -> int:
    authorization = request.headers.get("Authorization")
    if authorization is not None:
        scheme, separator, credentials = authorization.partition(" ")
        if not separator or scheme.lower() != "bearer" or not credentials.strip():
            raise _unauthorized()
        token = credentials.strip()
    else:
        token = request.cookies.get("access_token", "")

    if not token:
        raise _unauthorized()

    try:
        payload = jwt.decode(
            token,
            _jwt_secret(),
            algorithms=["HS256"],
            issuer=JWT_ISSUER,
            options={"require": ["sub", "iss", "iat", "exp"]},
        )
        subject = payload["sub"]
        if not isinstance(subject, str) or not subject.isdigit() or int(subject) < 1:
            raise _unauthorized()
    except (InvalidTokenError, KeyError, TypeError, ValueError) as exc:
        raise _unauthorized() from exc

    return int(subject)


def _get_authenticated_db_session(
    user_id: int = Depends(_get_user_id),
) -> Generator[Session, None, None]:
    if user_id < 1:
        raise _unauthorized()
    yield from get_db_session()


def get_current_user(
    user_id: int = Depends(_get_user_id),
    db: Session = Depends(_get_authenticated_db_session),
) -> UserProfile:
    profile = MemberRepository(db).get_user_profile_by_id(user_id)
    if profile is None:
        raise _unauthorized()
    return profile


get_current_member = get_current_user


def validate_auth_secrets() -> None:
    jwt_secret = settings.JWT_SECRET_KEY
    session_secret = settings.SESSION_SECRET_KEY
    if len(jwt_secret) < 32:
        raise RuntimeError("JWT_SECRET_KEY must contain at least 32 characters")
    if len(session_secret) < 32:
        raise RuntimeError("SESSION_SECRET_KEY must contain at least 32 characters")
    if jwt_secret == session_secret:
        raise RuntimeError("JWT_SECRET_KEY and SESSION_SECRET_KEY must be different")
    if settings.ACCESS_TOKEN_EXPIRE_SECONDS <= 0:
        raise RuntimeError("ACCESS_TOKEN_EXPIRE_SECONDS must be positive")


def _unauthorized() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )
