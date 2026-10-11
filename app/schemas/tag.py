from pydantic import BaseModel, ConfigDict, Field


class TagBase(BaseModel):
    tag_name: str = Field(max_length=100)
    tag_type: str | None = Field(default=None, max_length=50)


class TagCreate(TagBase):
    pass


class TagUpdate(BaseModel):
    tag_name: str | None = Field(default=None, max_length=100)
    tag_type: str | None = Field(default=None, max_length=50)


class TagResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tgid: int
    tag_name: str
    tag_type: str | None