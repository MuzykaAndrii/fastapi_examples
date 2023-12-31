from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
)


class OperationCreate(BaseModel):
    quantity: str
    figi: str
    instrument_type: str
    date: datetime
    type: str


class OperationRead(BaseModel):
    model_config: ConfigDict(from_attributes=True)

    id: int
    quantity: str
    figi: str
    instrument_type: str
    date: datetime
    type: str
