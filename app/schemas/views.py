from datetime import datetime

from pydantic import BaseModel


class TeamMemberViewResponse(BaseModel):
    tid: int
    team_name: str
    uid: int
    username: str
    email: str
    is_owner: bool
    joined_at: datetime


class AssetDetailViewResponse(BaseModel):
    aid: int
    asset_name: str
    description: str | None
    path: str
    poly_count: int
    vert_count: int
    texture_resolution: str | None
    is_pot: bool
    created_at: datetime
    owner_id: int
    owner_name: str
    team_id: int
    team_name: str