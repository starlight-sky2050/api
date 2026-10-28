from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.db import get_db_session
from app.models.permission import Permission
from app.models.user_team import UserTeam
from app.repositories.user_team_permission import UserTeamPermissionRepository
from app.schemas.user_team_permission import (
    GrantPermissionRequest,
    MemberPermissionResponse,
)

router = APIRouter(prefix="/api/team-permissions", tags=["team-permissions"])


@router.get(
    "/{tid}/members/{uid}",
    response_model=list[MemberPermissionResponse],
)
def get_member_permissions(
    tid: int,
    uid: int,
    session: Session = Depends(get_db_session),
) -> list[MemberPermissionResponse]:
    return UserTeamPermissionRepository(session).get_member_permissions(tid, uid)


@router.post(
    "/{tid}/members/{uid}",
    response_model=MemberPermissionResponse,
    status_code=status.HTTP_201_CREATED,
)
def grant_member_permission(
    tid: int,
    uid: int,
    request: GrantPermissionRequest,
    session: Session = Depends(get_db_session),
) -> MemberPermissionResponse:
    if session.get(UserTeam, (uid, tid)) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team member not found",
        )

    permission = session.get(Permission, request.pid)
    if permission is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permission not found",
        )

    try:
        UserTeamPermissionRepository(session).grant_permission(tid, uid, request.pid)
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Permission is already granted to this team member",
        ) from exc

    return MemberPermissionResponse(
        uid=uid,
        tid=tid,
        pid=permission.pid,
        pcode=permission.pcode,
    )


@router.delete(
    "/{tid}/members/{uid}/{pid}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
def revoke_member_permission(
    tid: int,
    uid: int,
    pid: int,
    session: Session = Depends(get_db_session),
) -> Response:
    if not UserTeamPermissionRepository(session).revoke_permission(tid, uid, pid):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team member permission not found",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
