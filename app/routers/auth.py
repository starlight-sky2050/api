from collections.abc import Mapping
from typing import Any

from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.db import get_db_session
from app.core.security import create_access_token, get_current_user
from app.repositories.member import MemberRepository, UserProfile

router = APIRouter(prefix="/api/auth", tags=["auth"])

oauth = OAuth()
oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


def _require_google_configuration() -> None:
    if not all(
        (
            settings.GOOGLE_CLIENT_ID,
            settings.GOOGLE_CLIENT_SECRET,
            settings.GOOGLE_REDIRECT_URI,
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Google authentication is not configured",
        )


@router.get("/google/login")
async def google_login(request: Request) -> RedirectResponse:
    _require_google_configuration()
    return await oauth.google.authorize_redirect(
        request,
        settings.GOOGLE_REDIRECT_URI,
    )


@router.get("/google/callback")
async def google_callback(
    request: Request,
    db: Session = Depends(get_db_session),
) -> RedirectResponse:
    _require_google_configuration()
    token = await oauth.google.authorize_access_token(request)
    userinfo: Any = token.get("userinfo")
    if not isinstance(userinfo, Mapping):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Google identity could not be verified",
        )

    google_sub = userinfo.get("sub")
    email = userinfo.get("email")
    email_verified = userinfo.get("email_verified")
    if (
        not isinstance(google_sub, str)
        or not google_sub
        or not isinstance(email, str)
        or not email
        or email_verified is not True
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="A verified Google email address is required",
        )

    name = userinfo.get("name")
    picture = userinfo.get("picture")
    user_id = MemberRepository(db).upsert_google_member(
        google_sub=google_sub,
        email=email,
        name=name if isinstance(name, str) else None,
        picture=picture if isinstance(picture, str) else None,
        email_verified=True,
    )
    access_token = create_access_token({"sub": user_id})
    response = RedirectResponse(
        url=settings.AUTH_SUCCESS_REDIRECT_URL,
        status_code=status.HTTP_303_SEE_OTHER,
    )
    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=settings.ACCESS_TOKEN_EXPIRE_SECONDS,
        httponly=True,
        secure=settings.AUTH_COOKIE_SECURE,
        samesite="lax",
        path="/",
    )
    return response


@router.get("/me")
def read_current_user(
    profile: UserProfile = Depends(get_current_user),
) -> UserProfile:
    return profile


@router.post("/logout")
def logout() -> Response:
    response = Response(
        content='{"message":"Logged out"}',
        media_type="application/json",
    )
    response.delete_cookie(
        key="access_token",
        secure=settings.AUTH_COOKIE_SECURE,
        httponly=True,
        samesite="lax",
        path="/",
    )
    return response
