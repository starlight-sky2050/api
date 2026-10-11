from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.permission import Permission


class PermissionRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all(self) -> list[Permission]:
        return list(self.session.scalars(select(Permission).order_by(Permission.pid)).all())

    def get_by_id(self, pid: int) -> Permission | None:
        return self.session.get(Permission, pid)

    def get_by_pcode(self, pcode: str) -> Permission | None:
        return self.session.scalar(select(Permission).where(Permission.pcode == pcode))

    def create(self, permission_data: dict[str, Any]) -> Permission:
        permission = Permission(**permission_data)
        self.session.add(permission)
        self.session.commit()
        self.session.refresh(permission)
        return permission

    def update(self, pid: int, permission_data: dict[str, Any]) -> Permission | None:
        permission = self.get_by_id(pid)
        if permission is None:
            return None

        for field, value in permission_data.items():
            setattr(permission, field, value)
        self.session.commit()
        self.session.refresh(permission)
        return permission

    def delete(self, pid: int) -> Permission | None:
        permission = self.get_by_id(pid)
        if permission is None:
            return None

        self.session.delete(permission)
        self.session.commit()
        return permission