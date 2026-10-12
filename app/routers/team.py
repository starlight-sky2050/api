from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.core.db import get_db_session
from app.repositories.team import TeamRepository
from app.schemas.team import AddTeamMemberRequest, TeamCreate, TeamResponse, TeamUpdate

router = APIRouter(prefix="/api/teams", tags=["teams"])


@router.post("", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
def create_team(
    team: TeamCreate,
    session: Session = Depends(get_db_session),
) -> TeamResponse:
    return TeamRepository(session).create(team.model_dump())


@router.get("", response_model=list[TeamResponse])
def get_teams(session: Session = Depends(get_db_session)) -> list[TeamResponse]:
    return TeamRepository(session).get_all()


@router.post("/{tid}/members", status_code=status.HTTP_201_CREATED)
def add_team_member(
    tid: int,
    member: AddTeamMemberRequest,
    session: Session = Depends(get_db_session),
) -> dict[str, str]:
    try:
        TeamRepository(session).add_member_via_function(tid, member.uid, member.is_owner)
    except Exception as exc:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    return {"message": "Team member added successfully"}


@router.get("/{tid}", response_model=TeamResponse)
def get_team(tid: int, session: Session = Depends(get_db_session)) -> TeamResponse:
    team = TeamRepository(session).get_by_id(tid)
    if team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    return team


@router.patch("/{tid}", response_model=TeamResponse)
def update_team(
    tid: int,
    team: TeamUpdate,
    session: Session = Depends(get_db_session),
) -> TeamResponse:
    updated_team = TeamRepository(session).update(
        tid, team.model_dump(exclude_unset=True)
    )
    if updated_team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    return updated_team


@router.delete("/{tid}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_team(tid: int, session: Session = Depends(get_db_session)) -> Response:
    deleted_team = TeamRepository(session).delete(tid)
    if deleted_team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)