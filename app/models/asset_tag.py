from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class AssetTag(Base):
    __tablename__ = "asset_tags"

    aid: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("assets.aid", ondelete="CASCADE"),
        primary_key=True,
    )
    tgid: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("tags.tgid", ondelete="CASCADE"),
        primary_key=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
