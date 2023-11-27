from typing import List, Union
import typing
from unittest import result
import strawberry as strawberryA
import uuid
from contextlib import asynccontextmanager

import datetime

from gql_publications.GraphResolvers import (
    resolvePublicationById,
    resolvePublicationAll,
    resolveAuthorById,
)
from gql_publications.GraphResolvers import (
    resolvePublicationTypeAll,
    resolvePublicationTypeById,
    resolvePublicationForPublicationType,
)
from gql_publications.GraphResolvers import (
    resolveUpdatePublication,
    resolveAuthorsForPublication,
    resolvePublicationsForSubject,
    resolveAuthorsByUser,
)

from typing import Optional

@strawberryA.federation.type(
    keys=["id"],
    description="""Entity representing a relation between an user and a publication""",
)
class AuthorGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveAuthorById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""order in author list""")
    def order(self) -> int:
        return self.order

    @strawberryA.field(description="""share on publication""")
    def share(self) -> float:
        return self.share

    @strawberryA.field(description="""user""")
    async def user(self) -> "UserGQLModel":
        return await UserGQLModel.resolve_reference(self.user_id)

    @strawberryA.field(description="""publication""")
    async def publication(self, info: strawberryA.types.Info) -> "PublicationGQLModel":
        return await PublicationGQLModel.resolve_reference(info, self.publication_id)

    @strawberryA.field(description="""If an author is valid""")
    def valid(self) -> bool:
        return self.valid

    @strawberryA.field(description="""last change""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange