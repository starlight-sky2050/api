from pydantic import BaseModel


class AssetTagCreate(BaseModel):
    tgid: int


class AssetTagResponse(BaseModel):
    aid: int
    tgid: int
    tag_name: str
    tag_type: str | None
