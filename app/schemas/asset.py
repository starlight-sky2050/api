from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AssetCreate(BaseModel):
    asset_name: str = Field(max_length=100)
    owner_id: int
    description: str | None = Field(default=None, max_length=500)
    path: str = Field(max_length=255)
    poly_count: int = 0
    vert_count: int = 0
    texture_resolution: str | None = Field(default=None, max_length=50)
    is_pot: bool = False


class AssetUpdate(BaseModel):
    asset_name: str | None = Field(default=None, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    path: str | None = Field(default=None, max_length=255)
    poly_count: int | None = None
    vert_count: int | None = None
    texture_resolution: str | None = Field(default=None, max_length=50)
    is_pot: bool | None = None


class AssetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    aid: int
    asset_name: str
    description: str | None
    path: str
    poly_count: int
    vert_count: int
    texture_resolution: str | None
    is_pot: bool
    created_at: datetime