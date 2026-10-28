from datetime import datetime

from sqlalchemy import Computed, DateTime, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("id", name="uq_users_id"),)

    uid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id: Mapped[int] = mapped_column(Integer, Computed("uid", persisted=True))
    display_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    username: Mapped[str | None] = mapped_column(String(100), nullable=True, unique=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True, unique=True)
    password: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)