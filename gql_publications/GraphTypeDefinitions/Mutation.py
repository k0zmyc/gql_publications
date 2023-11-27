from typing import List, Union
import typing
from unittest import result
import strawberry as strawberryA
import uuid
from contextlib import asynccontextmanager

def getLoaders(info):
    return info.context['all']

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

@strawberryA.federation.type(extend=True)
class Mutation:
    @strawberryA.mutation(description="Adds the authorship to the publication, Currently it does not check if the authorship exists.")
    async def author_insert(self, info: strawberryA.types.Info, author: AuthorInsertGQLModel) -> AuthorResultGQLModel:
        loader = getLoaders(info).authors
        row = await loader.insert(author)
        result = AuthorResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        return result

    @strawberryA.mutation(description="Updates the authorship.")
    async def author_update(self, info: strawberryA.types.Info, author: AuthorUpdateGQLModel) -> AuthorResultGQLModel:
        loader = getLoaders(info).authors
        row = await loader.update(author)
        result = AuthorResultGQLModel()
        result.msg = "ok"
        result.id = author.id
        if row is None:
            result.msg = "fail"
            
        return result

    @strawberryA.mutation(description="Delete the authorship.")
    async def author_delete(self, info: strawberryA.types.Info, authorship_id: strawberryA.ID) -> str:
        loader = getLoaders(info).authors
        await loader.delete(authorship_id)
        return "ok"

    @strawberryA.mutation(description="Create a new publication.")
    async def publication_insert(self, info: strawberryA.types.Info, publication: PublicationInsertGQLModel) -> PublicationResultGQLModel:
        loader = getLoaders(info).publications
        row = await loader.insert(publication)
        result = PublicationResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        return result

    @strawberryA.mutation(description="Update the publication.")
    async def publication_update(self, info: strawberryA.types.Info, publication: PublicationUpdateGQLModel) -> PublicationResultGQLModel:
        loader = getLoaders(info).publications
        row = await loader.update(publication)
        result = PublicationResultGQLModel()
        result.msg = "ok"
        result.id = publication.id
        if row is None:
            result.msg = "fail"
            
        return result