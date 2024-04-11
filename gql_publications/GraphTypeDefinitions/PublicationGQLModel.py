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
    resolve_date,
    resolve_publication_reference,
    resolve_valid,
    resolve_place,

    resolve_created,
    resolve_lastchange,
    resolve_createdby,
    resolve_changedby,
    resolve_rbacobject,

    createRootResolver_by_id
)

from gql_publications.GraphTypeDefinitions._GraphPermissions import RoleBasedPermission, OnlyForAuthentized

AuthorGQLModel = Annotated["AuthorGQLModel", strawberryA.lazy(".AuthorGQLModel")]
PublicationTypeGQLModel = Annotated["PublicationTypeGQLModel", strawberryA.lazy(".PublicationTypeGQLModel")]


@strawberryA.federation.type(
    keys=["id"],
    name = "PublicationGQLModel",
    description="""Entity representing a publication""",
)

class PublicationGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).publications
    
    id = resolve_id
    name = resolve_name
    published_date = resolve_date
    reference = resolve_publication_reference
    valid = resolve_valid
    place = resolve_place


    created = resolve_created
    lastchange = resolve_lastchange
    createdby = resolve_createdby
    changedby = resolve_changedby
    rbacobject = resolve_rbacobject
    

    @strawberryA.field(description="""Publication type""")
    async def publication_type(self, info: strawberryA.types.Info) -> Optional ["PublicationTypeGQLModel"]:
        from .PublicationTypeGQLModel import PublicationTypeGQLModel  # Import here to avoid circular dependency
        result = await PublicationTypeGQLModel.resolve_reference(info, self.publication_type_id)
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
class PublicationWhereFilter:
    name: str
    valid: bool
    createdby: uuid.UUID


@strawberryA.field(description="""Returns a list of publications""", permission_classes=[OnlyForAuthentized()])
async def publication_page(
    self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10,
    where: Optional[PublicationWhereFilter] = None
) -> List[PublicationGQLModel]:
    loader = getLoadersFromInfo(info).publications
    wf = None if where is None else strawberry.asdict(where)
    result = await loader.page(skip, limit, where = wf)
    return result


publication_by_id = createRootResolver_by_id(PublicationGQLModel, description="Returns publication by its id")

###########################################################################################################################
#                                                                                                                         #
#                                                       Models                                                            #
#                                                                                                                         #
###########################################################################################################################

from typing import Optional

@strawberryA.input(description="Definition of a publication used for creation")
class PublicationInsertGQLModel:
    id: Optional[uuid.UUID] = strawberryA.field(description="The ID of the publication", default=None)
    name: Optional[str] = strawberryA.field(description="Name/label of the publication")
    published_date: Optional[datetime.datetime] = strawberryA.field(description="Date of the publication creation", default=datetime.datetime.now())
    reference: Optional[str] = strawberryA.field(description="""Reference for the publication""", default=None)
    place: Optional[str] = strawberryA.field(description="""Place of publication origin""", default=None)
    valid: Optional[bool] = strawberryA.field(description="Indicates whether the publications data is valid or not (optional)", default=True)
    publication_type_id: uuid.UUID = strawberryA.field(description="The ID of the publication type")
    
@strawberryA.input(description="Definition of a publication used for update")
class PublicationUpdateGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the publication")
    lastchange: datetime.datetime = strawberry.field(description="Timestamp of last change")

    valid: Optional[bool] = strawberryA.field(description="Indicates whether the publications data is valid or not", default=None)
    name: Optional[str] = strawberryA.field(description="Updated name/label of the publication", default=None)
    publication_type_id: Optional[uuid.UUID] = strawberryA.field(description="The ID of the publication type",default=None)
    changedby: strawberry.Private[uuid.UUID] = None

@strawberryA.type(description="Result of a mutation for a publication")
class PublicationResultGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the publication", default=None)
    msg: str = strawberryA.field(description="Result of the operation (OK/Fail)", default=None)

    @strawberryA.field(description="Returns the publication")
    async def publication(self, info: strawberryA.types.Info) -> Union[PublicationGQLModel, None]:
        result = await PublicationGQLModel.resolve_reference(info, self.id)
        return result


###########################################################################################################################
#                                                                                                                         #
#                                                       Mutations                                                         #
#                                                                                                                         #
###########################################################################################################################

@strawberryA.mutation(description="Adds a new publication.",
                      permission_classes=[OnlyForAuthentized()])
async def publication_insert(self, info: strawberryA.types.Info, publication: PublicationInsertGQLModel) -> PublicationResultGQLModel:
    user = getUserFromInfo(info)
    publication.createdby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).publications
    row = await loader.insert(publication)
    result = PublicationResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result

@strawberryA.mutation(description="Update the publication.",
                      permission_classes=[OnlyForAuthentized()])
async def publication_update(self, info: strawberryA.types.Info, publication: PublicationUpdateGQLModel) -> PublicationResultGQLModel:
    user = getUserFromInfo(info)
    publication.changedby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).publications
    row = await loader.update(publication)
    result = PublicationResultGQLModel()
    result.msg = "ok"
    result.id = publication.id
    result.msg = "ok" if (row is not None) else "fail"
    return result


############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################

# @strawberryA.federation.type(
#     keys=["id"], description="""Entity representing an editable publication"""
# )
# class PublicationEditorGQLModel:

#     #
#     # Mutace, obejiti problemu s federativnim API
#     #
    

#     @classmethod
#     async def resolve_reference(cls, info: strawberryA.types.Info, id: uuid.UUID):
#         async with getLoadersFromInfo(info) as session:
#             result = await resolvePublicationById(session, id)
#             result._type_definition = cls._type_definition  # little hack :)
#             return result

#     @strawberryA.field(description="""Entity primary key""")
#     def id(self) -> uuid.UUID:
#         return self.id

#     @strawberryA.field(description="""Updates publication data""")
#     async def update(
#         self, info: strawberryA.types.Info, data: "PublicationUpdateGQLModel"
#     ) -> typing.Optional["PublicationGQLModel"]:
#         async with getLoadersFromInfo(info) as session:
#             result = await resolveUpdatePublication(session, id=self.id, data=data)
#             return result

#     @strawberryA.field(description="""Sets author a share""")
#     async def set_author_share(
#         self, info: strawberryA.types.Info, author_id: uuid.UUID, share: float
#     ) -> typing.Optional["AuthorGQLModel"]:
#         async with getLoadersFromInfo(info) as session:
#             result = await resolveUpdateAuthor(
#                 session, author_id, data=None, extraAttributes={"share": share}
#             )
#             return result

#     @strawberryA.field(description="""Updates the author data""")
#     async def set_author_order(
#         self, info: strawberryA.types.Info, author_id: uuid.UUID, order: int
#     ) -> List["AuthorGQLModel"]:
#         async with getLoadersFromInfo(info) as session:
#             result = await resolveUpdateAuthorOrder(session, self.id, author_id, order)
#             return result

#     @strawberryA.field(description="""Create a new author""")
#     async def add_author(
#         self, info: strawberryA.types.Info, user_id: uuid.UUID
#     ) -> typing.Optional["AuthorGQLModel"]:
#         async with getLoadersFromInfo(info) as session:
#             result = await resolveInsertAuthor(
#                 session,
#                 None,
#                 extraAttributes={"user_id": user_id, "publication_id": self.id},
#             )
#             return result

#     ######################
# @strawberryA.field(description="""Invalidate a publication""")
#     async def invalidate_publication(
#         self, info: strawberryA.types.Info
#     ) -> PublicationGQLModel:
#         async with getLoadersFromInfo(info) as session:
#             publication = await resolvePublicationById(session, self.id)
#             publication.valid = False
#             await session.commit()
#             return publication