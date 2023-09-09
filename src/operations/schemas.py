from datetime import datetime
from pydantic import BaseModel


class OperationCreate(BaseModel):
    quantity: str
    figi: str
    instrument_type: str
    date: datetime
    type: str


class OperationRead(BaseModel):    
    id: int
    quantity: str
    figi: str
    instrument_type: str
    date: datetime
    type: str

    class Config:
        orm_mode = True