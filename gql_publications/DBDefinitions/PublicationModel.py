import sqlalchemy

from sqlalchemy import (
    Column,
    String,
    DateTime,
    Uuid,
    Boolean,
    Date
)

from .base import BaseModel
from .uuid import UUIDColumn, UUIDFKey

class PublicationModel(BaseModel):

    """
    Represents a Publication entity in the database
    """

    __tablename__ = "publications"

    id = UUIDColumn()
    name = Column(String)
    published_date = Column(DateTime)
    reference = Column(String)
    valid = Column(Boolean)
    place = Column(String)

    publication_type_id = UUIDFKey(nullable=True, comment="ID of the publication type")#Column(Uuid, index=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True, comment="who's created the entity")#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True, comment="who's changed the entity")#Column(ForeignKey("users.id"), index=True, nullable=True)
    #rbacobject = UUIDFKey(nullable=True, comment="user or group id, determines access")