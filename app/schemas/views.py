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


class UserAssetViewResponse(BaseModel):
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


class TeamAssetViewResponse(BaseModel):
    tid: int
    team_name: str
    aid: int
    asset_name: str
    description: str | None
    path: str
    poly_count: int
    vert_count: int
    texture_resolution: str | None
    is_pot: bool
    asset_created_at: datetime
    shared_at: datetime
    owner_id: int
    owner_name: str