from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, func, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class Asset(Base):
    __tablename__ = "assets"

    aid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    asset_name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    path: Mapped[str] = mapped_column(String(255), nullable=False)
    poly_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default=text("0"))
    vert_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default=text("0"))
    texture_resolution: Mapped[str | None] = mapped_column(String(50), nullable=True)
    is_pot: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=text("false"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )