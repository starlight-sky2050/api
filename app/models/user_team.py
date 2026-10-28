from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class UserTeam(Base):
    __tablename__ = "user_teams"

    uid: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.uid", ondelete="CASCADE"),
        primary_key=True,
    )
    tid: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("teams.tid", ondelete="CASCADE"),
        primary_key=True,
    )
