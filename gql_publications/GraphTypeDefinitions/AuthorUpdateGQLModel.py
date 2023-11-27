from typing import List, Union
import typing
from unittest import result
import strawberry as strawberryA
import uuid
from contextlib import asynccontextmanager

import datetime

from typing import Optional

from gql_publications.DBFeeder import randomDataStructure

@strawberryA.input
class AuthorUpdateGQLModel:
    id: strawberryA.ID
    lastchange: datetime.datetime
    share: Optional[float] = None
    order: Optional[int] = None
    