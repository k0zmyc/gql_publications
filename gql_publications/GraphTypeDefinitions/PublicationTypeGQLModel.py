from typing import List, Union, Annotated
import typing
from unittest import result
import strawberry as strawberryA
import uuid
from contextlib import asynccontextmanager

from .BaseGQLModel import BaseGQLModel
from gql_publications.utils.Dataloaders import getLoadersFromInfo

from ._GraphResolvers import (
    resolvePublicationTypeById,
    resolvePublicationForPublicationType,
)

PublicationGQLModel = Annotated["PublicationGQLModel", strawberryA.lazy(".PublicationGQLModel")]

@strawberryA.type
class PublicationTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: uuid.UUID):
        async with getLoadersFromInfo(info) as session:
            result = await resolvePublicationTypeById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> uuid.UUID:
        return self.id

    @strawberryA.field(description="""type""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""List of publications with this type""")
    async def publications(
        self, info: strawberryA.types.Info
    ) -> typing.List["PublicationGQLModel"]:
        async with getLoadersFromInfo(info) as session:
            result = await resolvePublicationForPublicationType(session, self.id)
            return result