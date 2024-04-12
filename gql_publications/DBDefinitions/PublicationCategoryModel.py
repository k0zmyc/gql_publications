import sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from sqlalchemy import (
    Column,
    String,
    DateTime,
    Boolean
)

from .base import BaseModel
from .uuid import UUIDColumn, UUIDFKey


class PublicationCategoryModel(BaseModel):
    __tablename__ = "publicationcategories"

    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)


    valid = Column(Boolean, default=True, comment="Indicates whether this entity is valid or invalid")
    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True, comment="who's created the entity")#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True, comment="who's changed the entity")#Column(ForeignKey("users.id"), index=True, nullable=True)
    #rbacobject = UUIDFKey(nullable=True, comment="user or group id, determines access")