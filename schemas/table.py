from pydantic import BaseModel


class BaseTable(BaseModel):
    name: str
    seats: int
    location: str


class TableCreate(BaseTable):
    pass


class TableRead(BaseTable):
    id: int

    class Config:
        from_attributes = True


