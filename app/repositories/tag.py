from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.tag import Tag


class TagRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all(self) -> list[Tag]:
        return list(self.session.scalars(select(Tag).order_by(Tag.tgid)).all())

    def get_by_id(self, tgid: int) -> Tag | None:
        return self.session.get(Tag, tgid)

    def get_by_name(self, tag_name: str) -> Tag | None:
        return self.session.scalar(select(Tag).where(Tag.tag_name == tag_name))

    def create(self, tag_data: dict[str, Any]) -> Tag:
        tag = Tag(**tag_data)
        self.session.add(tag)
        self.session.commit()
        self.session.refresh(tag)
        return tag

    def update(self, tgid: int, tag_data: dict[str, Any]) -> Tag | None:
        tag = self.get_by_id(tgid)
        if tag is None:
            return None

        for field, value in tag_data.items():
            setattr(tag, field, value)
        self.session.commit()
        self.session.refresh(tag)
        return tag

    def delete(self, tgid: int) -> Tag | None:
        tag = self.get_by_id(tgid)
        if tag is None:
            return None

        self.session.delete(tag)
        self.session.commit()
        return tag