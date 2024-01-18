from typing import List, Union, Annotated
import typing
from unittest import result
import strawberry as strawberryA
import uuid
from contextlib import asynccontextmanager

from ._GraphResolvers import (
    resolvePublicationById,
    resolvePublicationAll,
    resolveAuthorById,
)
from ._GraphResolvers import (
    resolvePublicationTypeAll,
    resolvePublicationTypeById
)

AuthorGQLModel = Annotated["AuthorGQLModel", strawberryA.lazy(".AuthorGQLModel")]
PublicationGQLModel = Annotated["PublicationGQLModel", strawberryA.lazy(".PublicationGQLModel")]
PublicationTypeGQLModel = Annotated["PublicationTypeGQLModel", strawberryA.lazy(".PublicationTypeGQLModel")]



from gql_publications.utils.DBFeeder import randomDataStructure


@asynccontextmanager
async def withInfo(info):
    asyncSessionMaker = info.context["asyncSessionMaker"]
    async with asyncSessionMaker() as session:
        try:
            yield session
        finally:
            pass


def AsyncSessionFromInfo(info):
    print(
        "obsolete function used AsyncSessionFromInfo, use withInfo context manager instead"
    )
    return info.context["session"]

def getLoaders(info):
    return info.context['all']




@strawberryA.type(description="""Type for query root""")
class Query:
    @strawberryA.field(description="""Returns a list of publications (paged)""")
    async def publication_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[PublicationGQLModel]:
        async with withInfo(info) as session:
            result = await resolvePublicationAll(session, skip, limit)
            return result

    @strawberryA.field(description="""Finds a publication by their id""")
    async def publication_by_id(
        self, info: strawberryA.types.Info, id: uuid.UUID
    ) -> Union[PublicationGQLModel, None]:
        async with withInfo(info) as session:
            result = await resolvePublicationById(session, id)
            return result

    @strawberryA.field(description="""Finds an author by their id""")
    async def author_by_id(
        self, info: strawberryA.types.Info, id: uuid.UUID
    ) -> Union[AuthorGQLModel, None]:
        async with withInfo(info) as session:
            result = await resolveAuthorById(session, id)
            return result

    @strawberryA.field(description="""Gets a list of publication types""")
    async def publication_type_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[PublicationTypeGQLModel]:
        async with withInfo(info) as session:
            result = await resolvePublicationTypeAll(session, skip, limit)
            return result

    @strawberryA.field(description="""Finds a group type by its id""")
    async def publication_type_by_id(
        self, info: strawberryA.types.Info, id: uuid.UUID
    ) -> Union[PublicationTypeGQLModel, None]:
        async with withInfo(info) as session:
            result = await resolvePublicationTypeById(session, id)
            return result

    @strawberryA.field(description="""Random publications""")
    async def randomPublication(
        self, info: strawberryA.types.Info
    ) -> List[PublicationGQLModel]:
        async with withInfo(info) as session:
            result = await randomDataStructure(session)
            # print('random university id', newId)
            # result = await resolveGroupById(session,  newId)
            # print('db response', result.name)
            return result