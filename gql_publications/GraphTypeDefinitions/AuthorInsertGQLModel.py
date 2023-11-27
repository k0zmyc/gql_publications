from typing import List, Union
import typing
from unittest import result
import strawberry as strawberryA
import uuid
from contextlib import asynccontextmanager


from typing import Optional

from gql_publications.DBFeeder import randomDataStructure

@strawberryA.input
class AuthorInsertGQLModel:
    user_id: strawberryA.ID
    publication_id: strawberryA.ID
    id: Optional[strawberryA.ID] = None
    share: Optional[float] = 0.1
    order: Optional[int] = 1000
