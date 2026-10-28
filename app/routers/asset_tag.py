from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.db import get_db_session
from app.repositories.asset import AssetRepository
from app.repositories.asset_tag import AssetTagRepository
from app.repositories.tag import TagRepository
from app.schemas.asset_tag import AssetTagResponse

router = APIRouter(prefix="/api/asset-tags", tags=["asset-tags"])


@router.get("/{aid}", response_model=list[AssetTagResponse])
def get_tags_by_asset(
    aid: int,
    session: Session = Depends(get_db_session),
) -> list[AssetTagResponse]:
    if AssetRepository(session).get_by_id(aid) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found",
        )
    return AssetTagRepository(session).get_tags_by_asset(aid)


@router.post(
    "/{aid}/{tgid}",
    response_model=AssetTagResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_tag_to_asset(
    aid: int,
    tgid: int,
    session: Session = Depends(get_db_session),
) -> AssetTagResponse:
    if AssetRepository(session).get_by_id(aid) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found",
        )
    if TagRepository(session).get_by_id(tgid) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found",
        )

    try:
        AssetTagRepository(session).add_tag_to_asset(aid, tgid)
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Tag is already assigned to this asset",
        ) from exc

    tag = TagRepository(session).get_by_id(tgid)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found",
        )
    return AssetTagResponse(
        aid=aid,
        tgid=tag.tgid,
        tag_name=tag.tag_name,
        tag_type=tag.tag_type,
    )


@router.delete(
    "/{aid}/{tgid}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
def remove_tag_from_asset(
    aid: int,
    tgid: int,
    session: Session = Depends(get_db_session),
) -> Response:
    if not AssetTagRepository(session).remove_tag_from_asset(aid, tgid):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset tag association not found",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
