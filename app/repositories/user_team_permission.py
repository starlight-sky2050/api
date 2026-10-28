from sqlalchemy import delete, insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.permission import Permission
from app.models.user_team_permission import UserTeamPermission


class UserTeamPermissionRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def grant_permission(self, tid: int, uid: int, pid: int) -> None:
        try:
            self.session.execute(
                insert(UserTeamPermission).values(uid=uid, tid=tid, pid=pid)
            )
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise

    def revoke_permission(self, tid: int, uid: int, pid: int) -> bool:
        result = self.session.execute(
            delete(UserTeamPermission).where(
                UserTeamPermission.tid == tid,
                UserTeamPermission.uid == uid,
                UserTeamPermission.pid == pid,
            )
        )
        self.session.commit()
        return result.rowcount > 0

    def get_member_permissions(
        self, tid: int, uid: int
    ) -> list[dict[str, int | str]]:
        statement = (
            select(
                UserTeamPermission.uid,
                UserTeamPermission.tid,
                UserTeamPermission.pid,
                Permission.pcode,
            )
            .join(Permission, Permission.pid == UserTeamPermission.pid)
            .where(
                UserTeamPermission.tid == tid,
                UserTeamPermission.uid == uid,
            )
            .order_by(UserTeamPermission.pid)
        )
        return [dict(row) for row in self.session.execute(statement).mappings().all()]
