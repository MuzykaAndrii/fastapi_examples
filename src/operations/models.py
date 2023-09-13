from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
)
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Operation(Base):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True)
    quantity = Column(String)
    figi = Column(String)
    instrument_type = Column(String, nullable=True)
    date = Column(TIMESTAMP)
    type = Column(String)
