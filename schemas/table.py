from pydantic import BaseModel, ConfigDict


class BaseTable(BaseModel):
    name: str
    seats: int
    location: str


class TableCreate(BaseTable):
    pass


class TableRead(BaseTable):
    id: int

    model_config = ConfigDict(from_attributes=True)

