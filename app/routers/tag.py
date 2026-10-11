from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.core.db import get_db_session
from app.repositories.tag import TagRepository
from app.schemas.tag import TagCreate, TagResponse, TagUpdate

router = APIRouter(prefix="/api/tags", tags=["tags"])


@router.post("", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
def create_tag(
    tag: TagCreate,
    session: Session = Depends(get_db_session),
) -> TagResponse:
    return TagRepository(session).create(tag.model_dump())


@router.get("", response_model=list[TagResponse])
def get_tags(session: Session = Depends(get_db_session)) -> list[TagResponse]:
    return TagRepository(session).get_all()


@router.get("/{tgid}", response_model=TagResponse)
def get_tag(tgid: int, session: Session = Depends(get_db_session)) -> TagResponse:
    tag = TagRepository(session).get_by_id(tgid)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return tag


@router.patch("/{tgid}", response_model=TagResponse)
def update_tag(
    tgid: int,
    tag: TagUpdate,
    session: Session = Depends(get_db_session),
) -> TagResponse:
    updated_tag = TagRepository(session).update(
        tgid, tag.model_dump(exclude_unset=True)
    )
    if updated_tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return updated_tag


@router.delete("/{tgid}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_tag(tgid: int, session: Session = Depends(get_db_session)) -> Response:
    deleted_tag = TagRepository(session).delete(tgid)
    if deleted_tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)