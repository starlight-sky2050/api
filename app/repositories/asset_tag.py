from sqlalchemy import delete, insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.asset_tag import AssetTag
from app.models.tag import Tag


class AssetTagRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add_tag_to_asset(self, aid: int, tgid: int) -> None:
        try:
            self.session.execute(
                insert(AssetTag).values(aid=aid, tgid=tgid)
            )
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise

    def remove_tag_from_asset(self, aid: int, tgid: int) -> bool:
        result = self.session.execute(
            delete(AssetTag).where(AssetTag.aid == aid, AssetTag.tgid == tgid)
        )
        self.session.commit()
        return result.rowcount > 0

    def get_tags_by_asset(self, aid: int) -> list[dict[str, int | str | None]]:
        statement = (
            select(
                AssetTag.aid,
                AssetTag.tgid,
                Tag.tag_name,
                Tag.tag_type,
            )
            .join(Tag, Tag.tgid == AssetTag.tgid)
            .where(AssetTag.aid == aid)
            .order_by(AssetTag.tgid)
        )
        return [dict(row) for row in self.session.execute(statement).mappings().all()]
