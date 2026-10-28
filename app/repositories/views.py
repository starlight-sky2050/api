from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session


class ViewRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_team_members(self, tid: int) -> list[dict[str, Any]]:
        result = self.session.execute(
            text("SELECT * FROM v_team_members WHERE tid = :tid"), {"tid": tid}
        )
        return [dict(row) for row in result.mappings().all()]

    def get_user_assets(self, uid: int) -> list[dict[str, Any]]:
        result = self.session.execute(
            text("SELECT * FROM v_user_assets WHERE owner_id = :uid"), {"uid": uid}
        )
        return [dict(row) for row in result.mappings().all()]

    def get_team_assets(self, tid: int) -> list[dict[str, Any]]:
        result = self.session.execute(
            text("SELECT * FROM v_team_assets WHERE tid = :tid"), {"tid": tid}
        )
        return [dict(row) for row in result.mappings().all()]