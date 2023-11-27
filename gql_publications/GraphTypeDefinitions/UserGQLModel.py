from typing import List, Union
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


@strawberryA.federation.type(extend=True, keys=["id"])
class UserGQLModel:

    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: strawberryA.ID):
        return UserGQLModel(id=id)

    @strawberryA.field(description="""List of authors""")
    async def author_publications(
        self, info: strawberryA.types.Info
    ) -> typing.List["AuthorGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveAuthorsByUser(session, self.id)
            return result