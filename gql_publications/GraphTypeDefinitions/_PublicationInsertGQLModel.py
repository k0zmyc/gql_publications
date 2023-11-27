from typing import List, Union
import typing
from unittest import result
import strawberry as strawberryA
import uuid
from contextlib import asynccontextmanager

import datetime


from typing import Optional

@strawberryA.input
class _PublicationInsertGQLModel:
    id: Optional[strawberryA.ID] = None
    name: Optional[str] = None
    place: Optional[str] = None
    published_date: Optional[datetime.date] = None
    reference: Optional[str] = None
    publication_type_id: Optional[strawberryA.ID] = None
    valid: Optional[bool] = None