from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.core.db import get_db_session
from app.repositories.permission import PermissionRepository
from app.schemas.permission import PermissionCreate, PermissionResponse, PermissionUpdate

router = APIRouter(prefix="/api/permissions", tags=["permissions"])


@router.post("", response_model=PermissionResponse, status_code=status.HTTP_201_CREATED)
def create_permission(
    permission: PermissionCreate,
    session: Session = Depends(get_db_session),
) -> PermissionResponse:
    return PermissionRepository(session).create(permission.model_dump())


@router.get("", response_model=list[PermissionResponse])
def get_permissions(
    session: Session = Depends(get_db_session),
) -> list[PermissionResponse]:
    return PermissionRepository(session).get_all()


@router.get("/{pid}", response_model=PermissionResponse)
def get_permission(
    pid: int,
    session: Session = Depends(get_db_session),
) -> PermissionResponse:
    permission = PermissionRepository(session).get_by_id(pid)
    if permission is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found"
        )
    return permission


@router.patch("/{pid}", response_model=PermissionResponse)
def update_permission(
    pid: int,
    permission: PermissionUpdate,
    session: Session = Depends(get_db_session),
) -> PermissionResponse:
    updated_permission = PermissionRepository(session).update(
        pid, permission.model_dump(exclude_unset=True)
    )
    if updated_permission is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found"
        )
    return updated_permission


@router.delete(
    "/{pid}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response
)
def delete_permission(
    pid: int,
    session: Session = Depends(get_db_session),
) -> Response:
    deleted_permission = PermissionRepository(session).delete(pid)
    if deleted_permission is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)