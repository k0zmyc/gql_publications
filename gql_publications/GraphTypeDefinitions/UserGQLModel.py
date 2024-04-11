from typing import List, Union
import typing
import strawberry as strawberryA
import uuid
from contextlib import asynccontextmanager
import datetime
from typing import Annotated
from .BaseGQLModel import BaseGQLModel
from gql_publications.utils.Dataloaders import getLoadersFromInfo, getUserFromInfo
from ._GraphResolvers import (
    resolve_id,
    resolve_order,
    resolve_share,
    resolve_name,
    resolve_name_en,    
    resolve_user_id,
    resolve_created,
    resolve_lastchange,
    resolve_createdby,
    resolve_changedby,
    resolve_rbacobject,
    resolve_valid,
    createRootResolver_by_id,
   
)

from gql_publications.GraphTypeDefinitions._GraphPermissions import RoleBasedPermission, OnlyForAuthentized

PublicationGQLModel = Annotated["PublicationGQLModel", strawberryA.lazy(".PublicationGQLModel")]

@strawberryA.federation.type(extend=True, keys=["id"])
class UserGQLModel(BaseGQLModel):

    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).publications

    id = resolve_id
    name = resolve_name
    created = resolve_created
    lastchange = resolve_lastchange
    createdby = resolve_createdby
    changedby = resolve_changedby
    rbacobject = resolve_rbacobject
    valid = resolve_valid
    order = resolve_order
    share = resolve_share
    name_en = resolve_name_en
    user_id = resolve_user_id
    
    id: uuid.UUID = strawberryA.federation.field(external=True)
    
    @classmethod    
    async def resolve_reference(cls, id: uuid.UUID):
        return UserGQLModel(id=id)
    
    
    
    @strawberryA.field(description="List of publications for the user")
    async def publications(
        self, info: strawberryA.types.Info
    ) -> typing.List["PublicationGQLModel"]:
        loader = getLoadersFromInfo(info).publications
        result = await loader.filter_by(user_id = self.id)
        return result