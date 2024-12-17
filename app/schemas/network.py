from pydantic import BaseModel


class NetworkBase(BaseModel):
    name: str
    cidr: str
    description: str | None = None
    usage: str | None = None


class NetworkCreate(NetworkBase):
    pass


class NetworkResponse(NetworkBase):
    id: int
    name: str
    cidr: str
    description: str
    usage: str
    reserved_by: int

    class Config:
        orm_mode = True
