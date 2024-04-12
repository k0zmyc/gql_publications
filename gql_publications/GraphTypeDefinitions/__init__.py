###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################


import uuid
from typing import Union

import strawberry

#from .UserGQLModel import UserGQLModel
from .AuthorGQLModel import AuthorGQLModel
from .PublicationGQLModel import PublicationGQLModel
from .PublicationTypeGQLModel import PublicationTypeGQLModel
from .PublicationCategoryGQLModel import PublicationCategoryGQLModel
from .SubjectGQLModel import SubjectGQLModel

#from gql_publications.GraphTypeDefinitions._GraphPermissions import RoleBasedPermission

from .externals import UserGQLModel
from gql_publications.utils.Dataloaders import getUserFromInfo

@strawberry.type(description="""Type for query root""")
class Query:
    @strawberry.field(description="""Say hello to the world""")
    async def say_hello_publications(
        self, info: strawberry.types.Info, id: uuid.UUID
    ) -> Union[str, None]:
        user = getUserFromInfo(info)
        result = f"Hello {id} `{user}`"
        return result



    from .PublicationCategoryGQLModel import (
        publication_category_by_id,
        publication_category_page
    )
    publication_category_by_id = publication_category_by_id
    publication_category_page = publication_category_page

    from .PublicationGQLModel import (
        publication_by_id,
        publication_page
    )
    publication_by_id = publication_by_id
    publication_page = publication_page

    from .PublicationTypeGQLModel import (
        publication_type_by_id,
        publicationType_page
    )
    publication_type_by_id = publication_type_by_id
    publicationType_page = publicationType_page

    from .AuthorGQLModel import (
        author_by_id,
        author_page
    )
    author_by_id = author_by_id
    author_page = author_page

    from .SubjectGQLModel import (
        subject_by_id,
        subject_page
    )
    subject_by_id = subject_by_id
    subject_page = subject_page
        


    # from .UserGQLModel import (
    #     user_by_id,
    #     user_page
    # )
    # user_by_id = user_by_id
    # user_page = user_page



######################################################################################################################
#
#
# Mutations
#
#
######################################################################################################################

@strawberry.type(description="""Type for mutation root""")
class Mutation:
    

    from .PublicationCategoryGQLModel import (
        publicationCategory_insert,
        publicationCategory_update,
        #publicationCategory_delete
    )
    publicationCategory_insert = publicationCategory_insert
    publicationCategory_update = publicationCategory_update
    #publicationCategory_delete = publicationCategory_delete

    from .PublicationGQLModel import (
        publication_insert,
        publication_update,
        #publication_delete,
    )
    publication_insert = publication_insert
    publication_update = publication_update
    #publication_delete = publication_delete

    from .PublicationTypeGQLModel import (
        publicationType_insert,
        publicationType_update,
    )
    publicationType_insert = publicationType_insert
    publicationType_update = publicationType_update

    from .AuthorGQLModel import (
        author_insert,
        author_update,
        author_delete
    )
    author_insert = author_insert
    author_update = author_update
    author_delete = author_delete

    from .SubjectGQLModel import (
        subject_insert,
        subject_update,
        subject_delete
    )
    subject_insert = subject_insert
    subject_update = subject_update
    subject_delete = subject_delete
    
    
schema = strawberry.federation.Schema(Query, types=(PublicationGQLModel, PublicationCategoryGQLModel, 
                                                    PublicationTypeGQLModel, 
                                                    SubjectGQLModel, AuthorGQLModel),
                                      mutation=Mutation)


# schema = strawberryA.federation.Schema(Query, types=(PublicationGQLModel,), mutation=Mutation)