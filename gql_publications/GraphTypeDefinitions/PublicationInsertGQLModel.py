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
import datetime

@strawberryA.input
class PublicationInsertGQLModel:
    name: str
    
    id: Optional[strawberryA.ID] = None
    publication_type_id: Optional[strawberryA.ID] = None
    place: Optional[str] = ""
    published_date: Optional[datetime.datetime] = datetime.datetime.now()
    reference: Optional[str] = ""
    valid: Optional[bool] = True