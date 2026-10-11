from pydantic import BaseModel, ConfigDict, Field


class PermissionBase(BaseModel):
    pcode: str = Field(max_length=100)


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(BaseModel):
    pcode: str | None = Field(default=None, max_length=100)


class PermissionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    pid: int
    pcode: str