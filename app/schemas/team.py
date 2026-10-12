from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TeamBase(BaseModel):
    team_name: str = Field(max_length=100)
    description: str | None = Field(default=None, max_length=500)


class TeamCreate(TeamBase):
    invite_code: str | None = Field(default=None, max_length=50)


class TeamUpdate(BaseModel):
    team_name: str | None = Field(default=None, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    invite_code: str | None = Field(default=None, max_length=50)


class AddTeamMemberRequest(BaseModel):
    uid: int
    is_owner: bool = False


class TeamResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tid: int
    team_name: str
    description: str | None
    invite_code: str
    created_at: datetime