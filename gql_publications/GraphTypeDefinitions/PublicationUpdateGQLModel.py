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

from typing import Optional

from gql_publications.DBFeeder import randomDataStructure

@strawberryA.input
class PublicationUpdateGQLModel:
    lastchange: datetime.datetime
    id: strawberryA.ID

    name: Optional[str] = None
    publication_type_id: Optional[strawberryA.ID] = None
    place: Optional[str] = None
    published_date: Optional[datetime.datetime] = None
    reference: Optional[str] = None
    valid: Optional[bool] = None
    