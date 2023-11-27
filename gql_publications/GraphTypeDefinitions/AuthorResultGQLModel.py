from typing import List, Union, Annotated
import typing
from unittest import result
import strawberry as strawberryA
import uuid
from contextlib import asynccontextmanager

AuthorGQLModel = Annotated["AuthorGQLModel", strawberryA.lazy(".AuthorGQLModel")]
from gql_publications.DBFeeder import randomDataStructure

@strawberryA.type
class AuthorResultGQLModel:
    id: strawberryA.ID = None
    msg: str = None

    @strawberryA.field(description="""Result of publication operation""")
    async def author(self, info: strawberryA.types.Info) -> Union[AuthorGQLModel, None]:
        from .AuthorGQLModel import AuthorGQLModel
        result = await AuthorGQLModel.resolve_reference(info, self.id)
        return result