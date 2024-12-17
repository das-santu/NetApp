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
    reserved_by: int

    class Config:
        from_attributes = True


class NetworkUtilizationResponse(BaseModel):
    network: str
    total_ips: int
    used_ips: int
    reserved_percentage: float
    available_percentage: float

    class Config:
        from_attributes = True
