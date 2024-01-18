from typing import List, Union, Annotated
import typing
from unittest import result
import strawberry as strawberryA
import uuid
from contextlib import asynccontextmanager

from .BaseGQLModel import BaseGQLModel
from gql_publications.utils.Dataloaders import getLoadersFromInfo

from .PublicationGQLModel import PublicationUpdateGQLModel

from ._GraphResolvers import (
    resolvePublicationById
)
from ._GraphResolvers import (
    resolveUpdatePublication,
    resolveUpdateAuthor,
    resolveInsertAuthor,
    resolveUpdateAuthorOrder
)

AuthorGQLModel = Annotated["AuthorGQLModel", strawberryA.lazy(".AuthorGQLModel")]
PublicationGQLModel = Annotated["PublicationGQLModel", strawberryA.lazy(".PublicationGQLModel")]


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing an editable publication"""
)
class PublicationEditorGQLModel:

    ##
    ## Mutace, obejiti problemu s federativnim API
    ##
    

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: uuid.UUID):
        async with getLoadersFromInfo(info) as session:
            result = await resolvePublicationById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> uuid.UUID:
        return self.id

    @strawberryA.field(description="""Updates publication data""")
    async def update(
        self, info: strawberryA.types.Info, data: "PublicationUpdateGQLModel"
    ) -> typing.Optional["PublicationGQLModel"]:
        async with getLoadersFromInfo(info) as session:
            result = await resolveUpdatePublication(session, id=self.id, data=data)
            return result

    @strawberryA.field(description="""Sets author a share""")
    async def set_author_share(
        self, info: strawberryA.types.Info, author_id: uuid.UUID, share: float
    ) -> typing.Optional["AuthorGQLModel"]:
        async with getLoadersFromInfo(info) as session:
            result = await resolveUpdateAuthor(
                session, author_id, data=None, extraAttributes={"share": share}
            )
            return result

    @strawberryA.field(description="""Updates the author data""")
    async def set_author_order(
        self, info: strawberryA.types.Info, author_id: uuid.UUID, order: int
    ) -> List["AuthorGQLModel"]:
        async with getLoadersFromInfo(info) as session:
            result = await resolveUpdateAuthorOrder(session, self.id, author_id, order)
            return result

    @strawberryA.field(description="""Create a new author""")
    async def add_author(
        self, info: strawberryA.types.Info, user_id: uuid.UUID
    ) -> typing.Optional["AuthorGQLModel"]:
        async with getLoadersFromInfo(info) as session:
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
        async with getLoadersFromInfo(info) as session:
            publication = await resolvePublicationById(session, self.id)
            publication.valid = False
            await session.commit()
            return publication
