from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db import get_db_session
from app.repositories.views import ViewRepository
from app.schemas.views import AssetDetailViewResponse, TeamMemberViewResponse

router = APIRouter(prefix="/api/views", tags=["views"])


@router.get("/teams/{tid}/members", response_model=list[TeamMemberViewResponse])
def get_team_members(
    tid: int,
    session: Session = Depends(get_db_session),
) -> list[TeamMemberViewResponse]:
    return ViewRepository(session).get_team_members(tid)


@router.get("/assets/{aid}", response_model=AssetDetailViewResponse)
def get_asset_details(
    aid: int,
    session: Session = Depends(get_db_session),
) -> AssetDetailViewResponse:
    asset_details = ViewRepository(session).get_asset_details(aid)
    if asset_details is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Asset details not found"
        )
    return asset_details