from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class TeamAsset(Base):
    __tablename__ = "team_assets"

    tid: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("teams.tid", ondelete="CASCADE"),
        primary_key=True,
    )
    aid: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("assets.aid", ondelete="CASCADE"),
        primary_key=True,
    )
    shared_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
