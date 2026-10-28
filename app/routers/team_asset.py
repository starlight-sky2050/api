from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.db import get_db_session
from app.repositories.asset import AssetRepository
from app.repositories.team import TeamRepository
from app.repositories.team_asset import TeamAssetRepository
from app.schemas.team_asset import TeamAssetResponse

router = APIRouter(prefix="/api/team-assets", tags=["team-assets"])


@router.get("/{tid}", response_model=list[TeamAssetResponse])
def get_team_assets(
    tid: int,
    session: Session = Depends(get_db_session),
) -> list[TeamAssetResponse]:
    if TeamRepository(session).get_by_id(tid) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found",
        )
    return TeamAssetRepository(session).get_team_assets(tid)


@router.post(
    "/{tid}/{aid}",
    response_model=TeamAssetResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_asset_to_team(
    tid: int,
    aid: int,
    session: Session = Depends(get_db_session),
) -> TeamAssetResponse:
    if TeamRepository(session).get_by_id(tid) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found",
        )
    if AssetRepository(session).get_by_id(aid) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found",
        )

    try:
        return TeamAssetRepository(session).add_asset_to_team(tid, aid)
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Asset is already shared with this team",
        ) from exc


@router.delete(
    "/{tid}/{aid}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
def remove_asset_from_team(
    tid: int,
    aid: int,
    session: Session = Depends(get_db_session),
) -> Response:
    if not TeamAssetRepository(session).remove_asset_from_team(tid, aid):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team asset association not found",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
