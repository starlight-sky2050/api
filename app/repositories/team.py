import secrets
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.team import Team


class TeamRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all(self) -> list[Team]:
        return list(self.session.scalars(select(Team).order_by(Team.tid)).all())

    def get_by_id(self, tid: int) -> Team | None:
        return self.session.get(Team, tid)

    def get_by_invite_code(self, invite_code: str) -> Team | None:
        return self.session.scalar(select(Team).where(Team.invite_code == invite_code))

    def create(self, team_data: dict[str, Any]) -> Team:
        team_data = dict(team_data)
        if not team_data.get("invite_code"):
            invite_code = self._generate_invite_code()
            while self.get_by_invite_code(invite_code) is not None:
                invite_code = self._generate_invite_code()
            team_data["invite_code"] = invite_code

        team = Team(**team_data)
        self.session.add(team)
        self.session.commit()
        self.session.refresh(team)
        return team

    def update(self, tid: int, team_data: dict[str, Any]) -> Team | None:
        team = self.get_by_id(tid)
        if team is None:
            return None

        for field, value in team_data.items():
            setattr(team, field, value)
        self.session.commit()
        self.session.refresh(team)
        return team

    def delete(self, tid: int) -> Team | None:
        team = self.get_by_id(tid)
        if team is None:
            return None

        self.session.delete(team)
        self.session.commit()
        return team

    @staticmethod
    def _generate_invite_code() -> str:
        return secrets.token_urlsafe(32)