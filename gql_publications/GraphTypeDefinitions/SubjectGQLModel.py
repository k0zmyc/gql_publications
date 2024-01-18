from typing import List, Union, Annotated
import typing
from unittest import result
import strawberry as strawberryA
import uuid
from contextlib import asynccontextmanager

from .BaseGQLModel import BaseGQLModel
from gql_publications.utils.Dataloaders import getLoadersFromInfo

from ._GraphResolvers import (
    resolvePublicationsForSubject
)
PublicationGQLModel = Annotated["PublicationGQLModel", strawberryA.lazy(".PublicationGQLModel")]

@strawberryA.federation.type(extend=True, keys=["id"])
class SubjectGQLModel:

    @strawberryA.field(description="""primary key""")
    def id(self) -> uuid.UUID:
        return self.id
    
    @strawberryA.field(description="""primary key""")
    def publication_id(self) -> uuid.UUID:
        return self.publication_id

    @classmethod
    async def resolve_reference(cls, id: uuid.UUID):
        return SubjectGQLModel(id=id)