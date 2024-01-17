import sqlalchemy

from sqlalchemy import (
    Column,
    DateTime,
    Uuid
)

from .base import BaseModel
from .uuid import UUID, UUIDColumn, UUIDFKey

class SubjectModel(BaseModel):
    """Spojujici tabulka - predmet, publikace"""

    __tablename__ = "publication_subjects"

    id = UUIDColumn()
    publication_id = Column(Uuid, index=True)
    #subject_id = UUIDFKey(nullable=True)#Column(ForeignKey("plan_subjects.id"), index=True)

    #publication = relationship("PublicationModel")
    #subject = relationship("PlanSubjectModel")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True, comment="who's created the entity")#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True, comment="who's changed the entity")#Column(ForeignKey("users.id"), index=True, nullable=True)

    rbacobject = UUIDFKey(nullable=True, comment="user or group id, determines access")