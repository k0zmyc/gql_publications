from typing import List, Union, Annotated, Optional
import strawberry as strawberryA
import datetime
import typing
import uuid
import strawberry
from gql_publications.utils.Dataloaders import getLoadersFromInfo, getUserFromInfo
from .BaseGQLModel import BaseGQLModel


from ._GraphResolvers import (
    resolve_id,
    resolve_name,
    resolve_name_en,

    resolve_valid,

    resolve_created,
    resolve_lastchange,
    resolve_createdby,
    resolve_changedby,
    #resolve_rbacobject,
    
    createRootResolver_by_id,
)


#from gql_publications.GraphTypeDefinitions._GraphPermissions import RoleBasedPermission, OnlyForAuthentized

AuthorGQLModel = Annotated["AuthorGQLModel", strawberryA.lazy(".AuthorGQLModel")]


@strawberryA.federation.type(
    keys=["id"],
    name = "PublicationCategoryGQLModel",
    description="""Entity representing a publication category""",
)

class PublicationCategoryGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).publicationCategories
    
    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en

    valid = resolve_valid

    created = resolve_created
    lastchange = resolve_lastchange
    createdby = resolve_createdby
    changedby = resolve_changedby
    #rbacobject = resolve_rbacobject
        

###########################################################################################################################
#                                                                                                                         #
#                                                       Query                                                             #
#                                                                                                                         #
###########################################################################################################################

from contextlib import asynccontextmanager

from dataclasses import dataclass
from .utils import createInputs
@createInputs
@dataclass
class PublicationCategoryWhereFilter:
    id: uuid.UUID
    name: str
    name_en: str
    valid: bool
    
    createdby: uuid.UUID
    changedby: uuid.UUID

@strawberryA.field(description="""Returns a list of publication categories""")
async def publication_category_page(
    self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10,
    where: Optional[PublicationCategoryWhereFilter] = None
) -> List[PublicationCategoryGQLModel]:
    loader = getLoadersFromInfo(info).publicationCategories
    wf = None if where is None else strawberry.asdict(where)
    result = await loader.page(skip, limit, where = wf)
    return result


publication_category_by_id = createRootResolver_by_id(PublicationCategoryGQLModel, description="Returns publication category by its id")

###########################################################################################################################
#                                                                                                                         #
#                                                       Models                                                            #
#                                                                                                                         #
###########################################################################################################################

from typing import Optional

@strawberryA.input(description="Definition of a publication category used for creation")
class PublicationCategoryInsertGQLModel:
    id: Optional[uuid.UUID] = strawberryA.field(description="The ID of the publication category", default=None)
    name: Optional[str] = strawberryA.field(description="Name/label of the publication category")
    name_en: Optional[str] = strawberryA.field(description="Name/label of the publication category in English")
    valid: Optional[bool] = strawberryA.field(description="Indicates whether the publication categories data is valid or not (optional)", default=True)
    

    
@strawberryA.input(description="Definition of a publication category used for update")
class PublicationCategoryUpdateGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the publication category")
    lastchange: datetime.datetime = strawberry.field(description="Timestamp of last change")

    valid: Optional[bool] = strawberryA.field(description="Indicates whether the publication categories data is valid or not", default=None)
    name: Optional[str] = strawberryA.field(description="Updated name/label of the publication category", default=None)
    name_en: Optional[str] = strawberryA.field(description="Updated name/label of the publication category(in english)", default=None)
    publication_type_id: Optional[uuid.UUID] = strawberryA.field(description="The ID of the publication category type",default=None)
    changedby: strawberry.Private[uuid.UUID] = None

@strawberryA.type(description="Result of a mutation for a publication category")
class PublicationCategoryResultGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the publication category", default=None)
    msg: str = strawberryA.field(description="Result of the operation (OK/Fail)", default=None)

    @strawberryA.field(description="Returns the publication category")
    async def publication(self, info: strawberryA.types.Info) -> Union[PublicationCategoryGQLModel, None]:
        result = await PublicationCategoryGQLModel.resolve_reference(info, self.id)
        return result


###########################################################################################################################
#                                                                                                                         #
#                                                       Mutations                                                         #
#                                                                                                                         #
###########################################################################################################################

@strawberryA.mutation(description="Adds a new publicationCategory.")
async def publicationCategory_insert(self, info: strawberryA.types.Info, publicationCategory: PublicationCategoryInsertGQLModel) -> PublicationCategoryResultGQLModel:
    user = getUserFromInfo(info)
    publicationCategory.createdby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).publicationCategories
    row = await loader.insert(publicationCategory)
    result = PublicationCategoryResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result

@strawberryA.mutation(description="Update the publication category.")
async def publicationCategory_update(self, info: strawberryA.types.Info, publicationCategory: PublicationCategoryUpdateGQLModel) -> PublicationCategoryResultGQLModel:
    user = getUserFromInfo(info)
    publicationCategory.changedby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).publicationCategories
    row = await loader.update(publicationCategory)
    result = PublicationCategoryResultGQLModel()
    result.msg = "ok"
    result.id = publicationCategory.id
    result.msg = "ok" if (row is not None) else "fail"
    return result

@strawberry.mutation(
    description="Delete the publication category.")
async def publicationCategory_delete(self, info: strawberryA.types.Info, id: uuid.UUID) -> PublicationCategoryResultGQLModel:
    loader = getLoadersFromInfo(info).publicationCategories
    row = await loader.delete(id=id)
    result = PublicationCategoryResultGQLModel(id=id, msg="ok")
    result.msg = "fail" if row is None else "ok"
    return result