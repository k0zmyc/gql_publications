import sqlalchemy

from sqlalchemy import (
    Column,
    Uuid,
    DateTime,
    Integer,
    Float
)

from sqlalchemy.orm import relationship

from .base import BaseModel
from .uuid import UUIDColumn, UUIDFKey


class AuthorModel(BaseModel):
    __tablename__ = "publication_authors"

    id = UUIDColumn()
    user_id = Column(Uuid, index=True)
    publication_id = Column(Uuid, index=True)
    order = Column(Integer)
    share = Column(Float)

    #user = relationship("UserModel", back_populates="author")
    #publication = relationship("PublicationModel", back_populates="author")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)

