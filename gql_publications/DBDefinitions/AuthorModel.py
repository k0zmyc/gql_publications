import sqlalchemy

from sqlalchemy import (
    Column,
    Uuid,
    DateTime,
    Boolean,
    Integer,
    Float
)

from sqlalchemy.orm import relationship

from .base import BaseModel
from .uuid import UUIDColumn, UUIDFKey


class AuthorModel(BaseModel):
    __tablename__ = "publication_authors"

    id = UUIDColumn()
    order = Column(Integer)
    share = Column(Float)

    publication_id = UUIDFKey(nullable=True, comment="ID of the associated publication")#Column(Uuid, index=True)
    user_id = Column(Uuid, index=True)

    #user = relationship("UserModel", back_populates="author")
    #publication = relationship("PublicationModel", back_populates="author")

    valid = Column(Boolean, default=True, comment="Indicates whether this entity is valid or invalid")
    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    rbacobject = UUIDFKey(nullable=True, comment="user or group id, determines access")
    
