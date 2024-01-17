from typing import List, Union
import typing
from unittest import result
import strawberry as strawberryA
import uuid
from contextlib import asynccontextmanager

from .BaseGQLModel import BaseGQLModel
from gql_publications.utils.Dataloaders import getLoadersFromInfo

@strawberryA.federation.type(extend=True, keys=["id"])
class PlanSubjectGQLModel:

    id: uuid.UUID = strawberryA.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: uuid.UUID):
        return PlanSubjectGQLModel(id=id)