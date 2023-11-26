import sqlalchemy

from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    Boolean,
    Date
)

from .base import BaseModel
from .uuid import UUIDColumn, UUIDFKey

class PublicationModel(BaseModel):

    __tablename__ = "publications"

    id = UUIDColumn()
    name = Column(String)

    publication_type_id = Column(ForeignKey("publicationtypes.id"), index=True)
    place = Column(String)
    published_date = Column(Date)
    reference = Column(String)
    valid = Column(Boolean)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)

    #author = relationship("AuthorModel", back_populates="publication")
    #publication_type = relationship(
    #    "PublicationTypeModel", back_populates="publication"
    #)