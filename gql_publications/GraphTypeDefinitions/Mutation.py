from typing import List, Union, Annotated
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


def AsyncSessionFromInfo(info):
    print(
        "obsolete function used AsyncSessionFromInfo, use withInfo context manager instead"
    )
    return info.context["session"]

def getLoaders(info):
    return info.context['all']

AuthorInsertGQLModel = Annotated["AuthorInsertGQLModel", strawberryA.lazy(".AuthorGQLModel")]
AuthorUpdateGQLModel = Annotated["AuthorUpdateGQLModel", strawberryA.lazy(".AuthorGQLModel")]
AuthorResultGQLModel = Annotated["AuthorResultGQLModel", strawberryA.lazy(".AuthorGQLModel")]

PublicationInsertGQLModel = Annotated["PublicationInsertGQLModel", strawberryA.lazy(".PublicationGQLModel")]
PublicationResultGQLModel = Annotated["PublicationResultGQLModel", strawberryA.lazy(".PublicationGQLModel")]
PublicationUpdateGQLModel = Annotated["PublicationUpdateGQLModel", strawberryA.lazy(".PublicationGQLModel")]

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
    async def author_delete(self, info: strawberryA.types.Info, authorship_id: uuid.UUID) -> str:
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