from typing import List, Union, Annotated
import typing
from unittest import result
import strawberry as strawberryA
import uuid
from contextlib import asynccontextmanager

@asynccontextmanager
async def withInfo(info):
    asyncSessionMaker = info.context["asyncSessionMaker"]
    async with asyncSessionMaker() as session:
        try:
            yield session
        finally:
            pass


from gql_publications.GraphResolvers import (
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