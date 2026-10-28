from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, ForeignKeyConstraint, Integer, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class UserTeamPermission(Base):
    __tablename__ = "user_team_permissions"
    __table_args__ = (
        ForeignKeyConstraint(
            ["uid", "tid"],
            ["user_teams.uid", "user_teams.tid"],
            ondelete="CASCADE",
        ),
    )

    uid: Mapped[int] = mapped_column(Integer, primary_key=True)
    tid: Mapped[int] = mapped_column(Integer, primary_key=True)
    pid: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("permissions.pid", ondelete="CASCADE"),
        primary_key=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
