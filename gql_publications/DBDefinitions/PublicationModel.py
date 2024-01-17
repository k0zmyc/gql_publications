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

    __tablename__ = "publications"

    id = UUIDColumn()
    name = Column(String)

    publication_type_id = Column(Uuid, index=True)
    place = Column(String)
    published_date = Column(Date)
    reference = Column(String)
    valid = Column(Boolean)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    createdby = UUIDFKey(nullable=True, comment="who's created the entity")#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True, comment="who's changed the entity")#Column(ForeignKey("users.id"), index=True, nullable=True)

    rbacobject = UUIDFKey(nullable=True, comment="user or group id, determines access")

    #author = relationship("AuthorModel", back_populates="publication")
    #publication_type = relationship(
    #    "PublicationTypeModel", back_populates="publication"
    #)