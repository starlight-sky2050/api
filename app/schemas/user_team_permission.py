from pydantic import BaseModel


class GrantPermissionRequest(BaseModel):
    pid: int


class MemberPermissionResponse(BaseModel):
    uid: int
    tid: int
    pid: int
    pcode: str
