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
    resolve_rbacobject,
    createRootResolver_by_id
)

from gql_publications.GraphTypeDefinitions._GraphPermissions import RoleBasedPermission, OnlyForAuthentized

AuthorGQLModel = Annotated["AuthorGQLModel", strawberryA.lazy(".AuthorGQLModel")]
UserGQLModel = Annotated["UserGQLModel", strawberryA.lazy(".UserGQLModel")]
PublicationGQLModel = Annotated["PublicationGQLModel", strawberryA.lazy(".PublicationGQLModel")]
PublicationCategoryGQLModel = Annotated["PublicationCategoryGQLModel", strawberryA.lazy(".PublicationCategoryGQLModel")]


@strawberryA.federation.type(
    keys=["id"],
    name = "PublicationTypeGQLModel",
    description="""Entity representing a publicationType""",
)

class PublicationTypeGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).publicationTypes
    
    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en
    valid = resolve_valid
    created = resolve_created
    lastchange = resolve_lastchange
    createdby = resolve_createdby
    changedby = resolve_changedby
    rbacobject = resolve_rbacobject


    @strawberryA.field(description="""Returns a list of publicationTypes with the same type id""", permission_classes=[OnlyForAuthentized()])
    async def publicationType(
        self, info: strawberryA.types.Info
    ) -> List["PublicationTypeGQLModel"]:
        loader = getLoadersFromInfo(info).publicationtypes
        result = await loader.filter_by(publicaion_type_id=self.publication_type_id)
        return result
    

    @strawberryA.field(description="""Returns a list of authors, where the author participated in publication by type""", permission_classes=[OnlyForAuthentized()])
    async def authorsByPublicationType(
        self, info: strawberryA.types.Info
    ) -> typing.List["PublicationGQLModel"]:
        loader = getLoadersFromInfo(info).authors
        result = await loader.filter_by(publication_id=self.publication_type_id)
        return result
        

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
class PublicationTypeWhereFilter:
    name: str
    type_id: uuid.UUID
    value: str
    createdby: uuid.UUID
    valid: bool
    place: str
    published_date: datetime.datetime
    reference: str


@strawberryA.field(description="""Returns a list of publicationTypes""", permission_classes=[OnlyForAuthentized()])
async def publicationType_page(
    self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10,
    where: Optional[PublicationTypeWhereFilter] = None
) -> List[PublicationTypeGQLModel]:
    loader = getLoadersFromInfo(info).publicationtypes
    wf = None if where is None else strawberry.asdict(where)
    result = await loader.page(skip, limit, where = wf)
    return result


publication_type_by_id = createRootResolver_by_id(PublicationTypeGQLModel, description="Returns publication type by its id")

###########################################################################################################################
#                                                                                                                         #
#                                                       Models                                                            #
#                                                                                                                         #
###########################################################################################################################

from typing import Optional

@strawberryA.input(description="Definition of a publication used for creation")
class PublicationTypeInsertGQLModel:
    publication_type_id: uuid.UUID = strawberryA.field(description="The ID of the publicationType type")
    name: str = strawberryA.field(description="Name/label of the publicationType")
    
    valid: Optional[bool] = strawberryA.field(description="Indicates whether the publicationTypes data is valid or not (optional)", default=True)
    id: Optional[uuid.UUID] = strawberryA.field(description="The ID of the publicationType", default=None)
    content_id: Optional[uuid.UUID] = strawberryA.field(description="The ID of the content associated with the publicationType ", default=None)
    createdby: strawberry.Private[uuid.UUID] = None
    rbacobject: strawberry.Private[uuid.UUID] = None
    
@strawberryA.input(description="Definition of a publicationType used for update")
class PublicationTypeUpdateGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the publicationType")
    lastchange: datetime.datetime = strawberry.field(description="Timestamp of last change")

    valid: Optional[bool] = strawberryA.field(description="Indicates whether the publicationTypes data is valid or not", default=None)
    name: Optional[str] = strawberryA.field(description="Updated name/label of the publicationType", default=None)
    publication_type_id: Optional[uuid.UUID] = strawberryA.field(description="The ID of the publicationType type",default=None)
    changedby: strawberry.Private[uuid.UUID] = None

@strawberryA.type(description="Result of a mutation for a publicationType")
class PublicationTypeResultGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the publicationType", default=None)
    msg: str = strawberryA.field(description="Result of the operation (OK/Fail)", default=None)

    @strawberryA.field(description="Returns the publicationType")
    async def publicationType(self, info: strawberryA.types.Info) -> Union[PublicationTypeGQLModel, None]:
        result = await PublicationTypeGQLModel.resolve_reference(info, self.id)
        return result


###########################################################################################################################
#                                                                                                                         #
#                                                       Mutations                                                         #
#                                                                                                                         #
###########################################################################################################################

@strawberryA.mutation(description="Adds a new publicationType.",
                      permission_classes=[OnlyForAuthentized()])
async def publicationType_insert(self, info: strawberryA.types.Info, publication: PublicationTypeInsertGQLModel) -> PublicationTypeResultGQLModel:
    user = getUserFromInfo(info)
    publication.createdby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).publicationTypes
    row = await loader.insert(publication)
    result = PublicationTypeResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result

@strawberryA.mutation(description="Update the publicationType.",
                      permission_classes=[OnlyForAuthentized()])
async def publicationType_update(self, info: strawberryA.types.Info, publication: PublicationTypeUpdateGQLModel) -> PublicationTypeResultGQLModel:
    user = getUserFromInfo(info)
    publication.changedby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).publicationTypes
    row = await loader.update(publication)
    result = PublicationTypeResultGQLModel()
    result.msg = "ok"
    result.id = publication.id
    result.msg = "ok" if (row is not None) else "fail"
    return result