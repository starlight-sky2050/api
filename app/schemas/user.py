from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    username: str = Field(max_length=100)
    email: str = Field(max_length=255)


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: str | None = Field(default=None, max_length=100)
    email: str | None = Field(default=None, max_length=255)
    password: str | None = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uid: int
    username: str | None
    email: str | None
    created_at: datetime