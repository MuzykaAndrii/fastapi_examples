from datetime import datetime

from sqlalchemy import (
    MetaData,
    Table,
    Column,
    JSON,
    Integer,
    String,
    TIMESTAMP,
    ForeignKey,
)


metadata = MetaData()

role = Table(
    "role",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permissions", JSON)
)

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False),
    Column("username", String, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("registered_at", TIMESTAMP, default=datetime.utcnow),
    Column("role_id", Integer, ForeignKey(role.c.id)),
)