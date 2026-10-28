from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.core.db import get_db_session
from app.repositories.team import TeamRepository
from app.schemas.team import TeamCreate, TeamResponse, TeamUpdate

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