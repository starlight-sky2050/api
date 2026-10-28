from sqlalchemy import text
from sqlalchemy.orm import Session


class TeamMemberRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add_member_via_function(self, tid: int, uid: int, is_owner: bool) -> None:
        query = text("SELECT add_team_member(:tid, :uid, :is_owner)")
        self.session.execute(query, {"tid": tid, "uid": uid, "is_owner": is_owner})
        self.session.commit()

    def remove_member(self, tid: int, uid: int) -> bool:
        result = self.session.execute(
            text("DELETE FROM user_teams WHERE tid = :tid AND uid = :uid"),
            {"tid": tid, "uid": uid},
        )
        self.session.commit()
        return result.rowcount > 0
