from typing import List, Union, Annotated
import typing
from unittest import result
import strawberry as strawberryA
import uuid
from contextlib import asynccontextmanager

PublicationGQLModel = Annotated["PublicationGQLModel", strawberryA.lazy(".PublicationGQLModel")]

from typing import Optional

from gql_publications.DBFeeder import randomDataStructure

@strawberryA.type
class PublicationResultGQLModel:
    id: strawberryA.ID = None
    msg: str = None

    @strawberryA.field(description="""Result of publication operation""")
    async def publication(self, info: strawberryA.types.Info) -> Union[PublicationGQLModel, None]:
        result = await PublicationGQLModel.resolve_reference(info, self.id)
        return result
   