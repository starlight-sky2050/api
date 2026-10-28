from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.team_asset import TeamAsset


class TeamAssetRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add_asset_to_team(self, tid: int, aid: int) -> TeamAsset:
        team_asset = TeamAsset(tid=tid, aid=aid)
        self.session.add(team_asset)
        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise
        self.session.refresh(team_asset)
        return team_asset

    def remove_asset_from_team(self, tid: int, aid: int) -> bool:
        team_asset = self.session.get(TeamAsset, (tid, aid))
        if team_asset is None:
            return False

        self.session.delete(team_asset)
        self.session.commit()
        return True

    def get_team_assets(self, tid: int) -> list[TeamAsset]:
        statement = (
            select(TeamAsset)
            .where(TeamAsset.tid == tid)
            .order_by(TeamAsset.aid)
        )
        return list(self.session.scalars(statement).all())
