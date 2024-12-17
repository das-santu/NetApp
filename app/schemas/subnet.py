from pydantic import BaseModel


class SubnetBase(BaseModel):
    prefix: int
    description: str | None = None
    usage: str | None = None


class SubnetCreate(SubnetBase):
    network_id: int


class SubnetResponse(BaseModel):
    id: int
    subnet: str
    network_id: int
    reserved_by: int
    description: str
    usage: str

    class Config:
        from_attributes = True


class SubnetCalculator(BaseModel):
    network_cidr: str
    prefix_length: int
