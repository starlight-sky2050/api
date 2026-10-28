from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TeamAssetCreate(BaseModel):
    aid: int


class TeamAssetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tid: int
    aid: int
    shared_at: datetime
