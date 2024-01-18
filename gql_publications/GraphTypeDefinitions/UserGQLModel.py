from typing import List, Union, Annotated
import typing
from unittest import result
import strawberry as strawberryA
import uuid
from contextlib import asynccontextmanager

from .BaseGQLModel import BaseGQLModel
from gql_publications.utils.Dataloaders import getLoadersFromInfo

from ._GraphResolvers import (
    resolveAuthorsByUser
)

AuthorGQLModel = Annotated["AuthorGQLModel", strawberryA.lazy(".AuthorGQLModel")]


@strawberryA.federation.type(extend=True, keys=["id"])
class UserGQLModel:

    id: uuid.UUID = strawberryA.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: uuid.UUID):
        return UserGQLModel(id=id)

    @strawberryA.field(description="""List of authors""")
    async def author_publications(
        self, info: strawberryA.types.Info
    ) -> typing.List["AuthorGQLModel"]:
        async with getLoadersFromInfo(info) as session:
            result = await resolveAuthorsByUser(session, self.id)
            return result