import strawberry as strawberryA
import datetime
import uuid
from typing import List, Annotated, Optional, Union
from .BaseGQLModel import BaseGQLModel
import typing
from typing import Optional

import strawberry
from gql_publications.utils.Dataloaders import getLoadersFromInfo, getUserFromInfo


#from gql_publications.GraphTypeDefinitions._GraphPermissions import RoleBasedPermission, OnlyForAuthentized

from gql_publications.GraphTypeDefinitions._GraphResolvers import (
    resolve_id,
    resolve_order,
    resolve_share,
    resolve_user_id,
    resolve_valid,

    resolve_created,
    resolve_lastchange,
    resolve_createdby,
    resolve_changedby,
    #resolve_rbacobject,
    
    createRootResolver_by_id,
)

PublicationGQLModel = Annotated["PublicationGQLModel", strawberryA.lazy(".PublicationGQLModel")]

@strawberryA.federation.type(
    keys=["id"],
    description="""Entity representing a relation between an user and a publication""",
)
class AuthorGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).authors

    id = resolve_id
    order = resolve_order
    share = resolve_share
    user_id = resolve_user_id
    valid = resolve_valid

    changedby = resolve_changedby
    lastchange = resolve_lastchange
    created = resolve_created
    createdby = resolve_createdby
    #rbacobject = resolve_rbacobject


    @strawberryA.field(description="""Publication ID""")
    async def publication_id(self, info: strawberryA.types.Info) -> Optional ["PublicationGQLModel"]:
        from .PublicationGQLModel import PublicationGQLModel  # Import here to avoid circular dependency
        result = await PublicationGQLModel.resolve_reference(info, self.publication_id)
        return result
    
###########################################################################################################################
#                                                                                                                         #
#                                                       Query                                                             #
#                                                                                                                         #
###########################################################################################################################
    
from dataclasses import dataclass
from .utils import createInputs
@createInputs
@dataclass
class AuthorWhereFilter:
    id: uuid.UUID
    user_id: uuid.UUID
    publication_id:uuid.UUID
    order: int
    share: float
    valid: bool
    createdby: uuid.UUID

@strawberryA.field(description="""Returns a list of Authors""")
async def author_page(
    self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10,
    where: Optional[AuthorWhereFilter] = None
) -> List[AuthorGQLModel]:
    loader = getLoadersFromInfo(info).authors
    wf = None if where is None else strawberry.asdict(where)
    result = await loader.page(skip, limit, where = wf)
    return result

author_by_id = createRootResolver_by_id(AuthorGQLModel, description="Returns Author by id")

###########################################################################################################################
#                                                                                                                         #
#                                                       Models                                                            #
#                                                                                                                         #
###########################################################################################################################

@strawberryA.input(description="Definition of Author data used for creation")
class AuthorInsertGQLModel:
    publication_id: uuid.UUID = strawberryA.field(description="The ID of the associated publication")
    user_id: uuid.UUID = strawberryA.field(description="The ID of the associated user")

    order: Optional[int] = strawberryA.field(description="The order of the Author in the publication")
    share: Optional[float] = strawberryA.field(description="The share of the Author in the publication",default=None)
    valid: Optional[bool] = strawberryA.field(description="Indicates whether the data is valid or not (optional)", default=True)
    createdby: strawberry.Private[uuid.UUID] = None
    #rbacobject: strawberry.Private[uuid.UUID] = None

@strawberryA.input(description="Definition of Author data used for update")
class AuthorUpdateGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the Author data")
    lastchange: datetime.datetime = strawberry.field(description="Timestamp of last change")

    valid: Optional[bool] = strawberryA.field(description="Indicates whether the data is valid or not (optional)", default=None)
    user_id: Optional[uuid.UUID] = strawberryA.field(description="The ID of the data type",default=None)
    order: Optional[int] = strawberryA.field(description="The order of the Author in the publication")
    share: Optional[float] = strawberryA.field(description="The share of the Author in the publication",default=None)
    changedby: strawberry.Private[uuid.UUID] = None
    
@strawberryA.type(description="Result of a author information operation")
class AuthorResultGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the data", default=None)
    msg: str = strawberryA.field(description="Result of the operation (OK/Fail)", default=None)

    @strawberryA.field(description="Returns the data")
    async def author(self, info: strawberryA.types.Info) -> Union[AuthorGQLModel, None]:
        result = await AuthorGQLModel.resolve_reference(info, self.id)
        return result

###########################################################################################################################
#                                                                                                                         #
#                                                       Mutations                                                         #
#                                                                                                                         #
###########################################################################################################################
    

@strawberryA.mutation(description="Adds a new Author.")
async def author_insert(self, info: strawberryA.types.Info, author: AuthorInsertGQLModel) -> AuthorResultGQLModel:
    user = getUserFromInfo(info)
    author.changedby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).authors
    row = await loader.insert(author)
    result = AuthorResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result

@strawberryA.mutation(description="Update the Author.")
async def author_update(self, info: strawberryA.types.Info, author: AuthorUpdateGQLModel) -> AuthorResultGQLModel:
    user = getUserFromInfo(info)
    author.changedby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).authors
    row = await loader.update(author)
    result = AuthorResultGQLModel()
    result.msg = "ok"
    result.id = author.id
    result.msg = "ok" if (row is not None) else "fail"
    return result

@strawberry.mutation(description="Delete the Author.",)
async def author_delete(self, info: strawberryA.types.Info, id:uuid.UUID, 
    lastchange: datetime.datetime = strawberry.field()) -> AuthorResultGQLModel:
    loader = getLoadersFromInfo(info).authors
    row = await loader.delete(id=id)
    result = AuthorResultGQLModel(id=id, msg="ok")
    result.msg = "fail" if row is None else "ok"
    return result