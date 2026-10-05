from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.core.db import get_db_session
from app.repositories.asset import AssetRepository
from app.schemas.asset import AssetCreate, AssetResponse, AssetUpdate

router = APIRouter(prefix="/api/assets", tags=["assets"])


@router.post("", response_model=AssetResponse, status_code=status.HTTP_201_CREATED)
def create_asset(
    asset: AssetCreate,
    session: Session = Depends(get_db_session),
) -> AssetResponse:
    return AssetRepository(session).create(asset.model_dump())


@router.get("", response_model=list[AssetResponse])
def get_assets(session: Session = Depends(get_db_session)) -> list[AssetResponse]:
    return AssetRepository(session).get_all()


@router.get("/{aid}", response_model=AssetResponse)
def get_asset(aid: int, session: Session = Depends(get_db_session)) -> AssetResponse:
    asset = AssetRepository(session).get_by_id(aid)
    if asset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")
    return asset


@router.patch("/{aid}", response_model=AssetResponse)
def update_asset(
    aid: int,
    asset: AssetUpdate,
    session: Session = Depends(get_db_session),
) -> AssetResponse:
    updated_asset = AssetRepository(session).update(
        aid, asset.model_dump(exclude_unset=True)
    )
    if updated_asset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")
    return updated_asset


@router.delete("/{aid}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_asset(aid: int, session: Session = Depends(get_db_session)) -> Response:
    deleted_asset = AssetRepository(session).delete(aid)
    if deleted_asset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)