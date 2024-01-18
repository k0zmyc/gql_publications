from typing import List, Union, Annotated
import typing
from unittest import result
import strawberry as strawberryA
import uuid
from contextlib import asynccontextmanager
from typing import Optional
import datetime

from .BaseGQLModel import BaseGQLModel
from gql_publications.utils.Dataloaders import getLoadersFromInfo

from ._GraphResolvers import (resolveAuthorById)
from gql_publications.utils.DBFeeder import randomDataStructure

UserGQLModel = Annotated["UserGQLModel", strawberryA.lazy(".UserGQLModel")]
PublicationGQLModel = Annotated["PublicationGQLModel", strawberryA.lazy(".PublicationGQLModel")]

@strawberryA.federation.type(
    keys=["id"],
    description="""Entity representing a relation between an user and a publication""",
)
class AuthorGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: uuid.UUID):
        async with getLoadersFromInfo(info) as session:
            result = await resolveAuthorById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> uuid.UUID:
        return self.id

    @strawberryA.field(description="""order in author list""")
    def order(self) -> int:
        return self.order

    @strawberryA.field(description="""share on publication""")
    def share(self) -> float:
        return self.share

    @strawberryA.field(description="""user""")
    async def user(self) -> typing.Optional[uuid.UUID]:
        from .UserGQLModel import UserGQLModel
        return await UserGQLModel.resolve_reference(self.user_id)

    @strawberryA.field(description="""publication""")
    async def publication(self, info: strawberryA.types.Info) -> typing.Optional[uuid.UUID]:
        from .PublicationGQLModel import PublicationGQLModel
        return await PublicationGQLModel.resolve_reference(info, self.publication_id)

    @strawberryA.field(description="""If an author is valid""")
    def valid(self) -> bool:
        return self.valid

    @strawberryA.field(description="""last change""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange
    

@strawberryA.input(description="""Input structure - C operation""")
class AuthorInsertGQLModel:
    user_id: uuid.UUID
    publication_id: uuid.UUID
    id: Optional[uuid.UUID] = None
    share: Optional[float] = 0.1
    order: Optional[int] = 1000



@strawberryA.input(description="""Input structure - U operation""")
class AuthorUpdateGQLModel:
    id: uuid.UUID
    lastchange: datetime.datetime
    share: Optional[float] = None
    order: Optional[int] = None



@strawberryA.type
class AuthorResultGQLModel:
    id: uuid.UUID = None
    msg: str = None

    @strawberryA.field(description="""Result of publication operation""")
    async def author(self, info: strawberryA.types.Info) -> Union[AuthorGQLModel, None]:
        from .AuthorGQLModel import AuthorGQLModel
        result = await AuthorGQLModel.resolve_reference(info, self.id)
        return result