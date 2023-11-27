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

from .AuthorGQLModel import AuthorGQLModel
from .AuthorInsertGQLModel import AuthorInsertGQLModel
from .AuthorUpdateGQLModel import AuthorUpdateGQLModel
from .AuthorResultGQLModel import AuthorResultGQLModel
from .Mutation import Mutation
from .Query import Query
from .PlanSubjectGQLModel import PlanSubjectGQLModel
from .SubjectGQLModel import SubjectGQLModel
from .UserGQLModel import UserGQLModel
from ._PublicationInsertGQLModel import _PublicationInsertGQLModel
from ._PublicationUpdateGQLModel import _PublicationUpdateGQLModel
from .PublicationInsertGQLModel import PublicationInsertGQLModel
from .PublicationGQLModel import PublicationGQLModel
from .PublicationEditorGQLModel import PublicationEditorGQLModel
from .PublicationResultGQLModel import PublicationResultGQLModel
from .PublicationUpdateGQLModel import PublicationUpdateGQLModel
from .PublicationTypeGQLModel import PublicationTypeGQLModel

from typing import Optional

from gql_publications.DBFeeder import randomDataStructure


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
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[PublicationGQLModel, None]:
        async with withInfo(info) as session:
            result = await resolvePublicationById(session, id)
            return result

    @strawberryA.field(description="""Finds an author by their id""")
    async def author_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
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
        self, info: strawberryA.types.Info, id: strawberryA.ID
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