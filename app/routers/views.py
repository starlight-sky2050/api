from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db_session
from app.repositories.views import ViewRepository
from app.schemas.views import (
    TeamAssetViewResponse,
    TeamMemberViewResponse,
    UserAssetViewResponse,
)

router = APIRouter(prefix="/api/views", tags=["views"])


@router.get("/teams/{tid}/members", response_model=list[TeamMemberViewResponse])
def get_team_members(
    tid: int,
    session: Session = Depends(get_db_session),
) -> list[TeamMemberViewResponse]:
    return ViewRepository(session).get_team_members(tid)


@router.get("/users/{uid}/assets", response_model=list[UserAssetViewResponse])
def get_user_assets(
    uid: int,
    session: Session = Depends(get_db_session),
) -> list[UserAssetViewResponse]:
    return ViewRepository(session).get_user_assets(uid)


@router.get("/teams/{tid}/assets", response_model=list[TeamAssetViewResponse])
def get_team_assets(
    tid: int,
    session: Session = Depends(get_db_session),
) -> list[TeamAssetViewResponse]:
    return ViewRepository(session).get_team_assets(tid)