from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.core.db import get_db_session
from app.repositories.team_member import TeamMemberRepository
from app.schemas.team_member import AddTeamMemberRequest

router = APIRouter(prefix="/api/teams", tags=["team-members"])


@router.post("/{tid}/members", status_code=status.HTTP_201_CREATED)
def add_team_member(
    tid: int,
    member: AddTeamMemberRequest,
    session: Session = Depends(get_db_session),
) -> dict[str, str]:
    try:
        TeamMemberRepository(session).add_member_via_function(
            tid, member.uid, member.is_owner
        )
    except Exception as exc:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    return {"message": "Team member added successfully"}


@router.delete(
    "/{tid}/members/{uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
def remove_team_member(
    tid: int,
    uid: int,
    session: Session = Depends(get_db_session),
) -> Response:
    if not TeamMemberRepository(session).remove_member(tid, uid):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team member not found",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
