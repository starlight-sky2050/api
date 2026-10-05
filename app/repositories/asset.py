from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.asset import Asset


class AssetRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all(self) -> list[Asset]:
        return list(self.session.scalars(select(Asset).order_by(Asset.aid)).all())

    def get_by_id(self, aid: int) -> Asset | None:
        return self.session.get(Asset, aid)

    def create(self, asset_data: dict[str, Any]) -> Asset:
        asset = Asset(**asset_data)
        self.session.add(asset)
        self.session.commit()
        self.session.refresh(asset)
        return asset

    def update(self, aid: int, asset_data: dict[str, Any]) -> Asset | None:
        asset = self.get_by_id(aid)
        if asset is None:
            return None

        for field, value in asset_data.items():
            setattr(asset, field, value)
        self.session.commit()
        self.session.refresh(asset)
        return asset

    def delete(self, aid: int) -> Asset | None:
        asset = self.get_by_id(aid)
        if asset is None:
            return None

        self.session.delete(asset)
        self.session.commit()
        return asset