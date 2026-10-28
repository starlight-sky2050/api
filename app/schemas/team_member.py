from pydantic import BaseModel


class AddTeamMemberRequest(BaseModel):
    uid: int
    is_owner: bool = False
