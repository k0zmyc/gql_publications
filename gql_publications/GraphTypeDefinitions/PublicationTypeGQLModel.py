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



class PublicationTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolvePublicationTypeById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""type""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""List of publications with this type""")
    async def publications(
        self, info: strawberryA.types.Info
    ) -> typing.List["PublicationGQLModel"]:
        async with withInfo(info) as session:
            result = await resolvePublicationForPublicationType(session, self.id)
            return result


