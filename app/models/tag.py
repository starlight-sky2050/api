from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class Tag(Base):
    __tablename__ = "tags"

    tgid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tag_name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    tag_type: Mapped[str | None] = mapped_column(String(50), nullable=True)