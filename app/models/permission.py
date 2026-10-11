from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class Permission(Base):
    __tablename__ = "permissions"

    pid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pcode: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)