import sqlalchemy

from sqlalchemy import (
    Column,
    String,
    DateTime,
    Uuid
)

from .base import BaseModel
from .uuid import UUIDColumn, UUIDFKey

class PublicationTypeModel(BaseModel):
    __tablename__ = "publicationtypes"

    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)

    category_id = Column(Uuid, index=True, nullable=True)
    #publication = relationship("PublicationModel", back_populates="publication_type")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    #createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    #changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)

