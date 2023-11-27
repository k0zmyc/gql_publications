from typing import List, Union
import typing
from unittest import result
import strawberry as strawberryA
import uuid
from contextlib import asynccontextmanager

from .PublicationGQLModel import PublicationGQLModel

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
   