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

    def get_asset_details(self, aid: int) -> dict[str, Any] | None:
        result = self.session.execute(
            text("SELECT * FROM v_asset_details WHERE aid = :aid"), {"aid": aid}
        )
        row = result.mappings().first()
        return dict(row) if row is not None else None