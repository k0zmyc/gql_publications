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
    resolveUpdateAuthor,
    resolveInsertAuthor,
    resolveUpdateAuthorOrder
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



@strawberryA.federation.type(
    keys=["id"], description="""Entity representing an editable publication"""
)
class PublicationEditorGQLModel:

    ##
    ## Mutace, obejiti problemu s federativnim API
    ##
    

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolvePublicationById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Updates publication data""")
    async def update(
        self, info: strawberryA.types.Info, data: "PublicationUpdateGQLModel"
    ) -> "PublicationGQLModel":
        async with withInfo(info) as session:
            result = await resolveUpdatePublication(session, id=self.id, data=data)
            return result

    @strawberryA.field(description="""Sets author a share""")
    async def set_author_share(
        self, info: strawberryA.types.Info, author_id: strawberryA.ID, share: float
    ) -> "AuthorGQLModel":
        async with withInfo(info) as session:
            result = await resolveUpdateAuthor(
                session, author_id, data=None, extraAttributes={"share": share}
            )
            return result

    @strawberryA.field(description="""Updates the author data""")
    async def set_author_order(
        self, info: strawberryA.types.Info, author_id: strawberryA.ID, order: int
    ) -> List["AuthorGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveUpdateAuthorOrder(session, self.id, author_id, order)
            return result

    @strawberryA.field(description="""Create a new author""")
    async def add_author(
        self, info: strawberryA.types.Info, user_id: strawberryA.ID
    ) -> "AuthorGQLModel":
        async with withInfo(info) as session:
            result = await resolveInsertAuthor(
                session,
                None,
                extraAttributes={"user_id": user_id, "publication_id": self.id},
            )
            return result

    #######################

    @strawberryA.field(description="""Invalidate a publication""")
    async def invalidate_publication(
        self, info: strawberryA.types.Info
    ) -> PublicationGQLModel:
        async with withInfo(info) as session:
            publication = await resolvePublicationById(session, self.id)
            publication.valid = False
            await session.commit()
            return publication
