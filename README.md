# PUBLICATIONS_A

## Zadání:
* rozšiřte datové struktury (tabulky) způsobem, který umožní uložit specifické údaje k publikacím typu:
  - B: Odborná kniha

  - D: Stať ve sborníku

  - J: Recenzovaný odborný článek (Jimp, Jsc a Jost)

* Použijte https://www.vyzkum.cz/storage/att/338DAF8D743C561ADC66E8E392AE2F2A/StrukturyXML_2018_2.6.0.pdf str. 24-41
* Pro jednotlivé typy vytvořte GQLModely, propojte s entitou PublicationGQLModel
* Modely v databázi pomocí SQLAlchemy, API endpoint typu GraphQL s pomocí knihovny Strawberry.
* Přístup k databázi řešte důsledně přes AioDataloder, resp. (https://github.com/hrbolek/uoishelpers/blob/main/uoishelpers/dataloaders.py).
* Zabezpečte kompletní **C**R**UD** operace nad entitami ExternalIdModel, ExternalIdTypeModel, ExternalIdCategoryModel
* **CUD** operace jako návratový typ nejméně se třemi prvky id, msg a „entityresult“ (pojmenujte adekvátně podle dotčené entity), vhodné přidat možnost nadřízené entity, speciálně pro operaci **D**.
* Řešte autorizaci operací (permission classes).
* Kompletní CRUD dotazy na GQL v souboru externalids_queries.json (dictionary), jméno klíče nechť vhodně identifikuje operaci, hodnota je dictionary s klíči query (obsahuje parametrický dotaz) nebo mutation (obsahuje parametrické mutation) a variables (obsahuje dictionary jako testovací hodnoty).
* Kompletní popisy API v kódu (description u GQLModelů) a popisy DB vrstvy (comment u DBModelů).
* Zabezpečte více jak 90% code test coverage (standard pytest).
* 1PD OK

## Časový harmonogram:

9.10.2023 zveřejnění harmonogramu prací na projektu (z pohledu programátora), určení repository url (nebo alespoň root např. https://github.com/hrbolek)<br>
16.10.2023 projektový den, Prezentace porozumění projektu, jeho struktura, deskripce entit („live dokumentace v GQL API – Voyager / GraphiQL“)<br>
27.11.2023 projektový den, Prezentace alespoň RU operací<br>
15.1.2024 projektový den, Alfa verze<br>
21.1.2024 uzavření projektu<br>
22.1.2024 počátek zkouškového období<br>
?.3.2024 konec zkouškového období.<br>





# ISDatabase
Database backend for university site. Project is based on SQLAlchemy and GraphQL (strawberry federated).
<br/><br/>
This project contains only SQLAlchemy models and GraphQL endpoint to provide data from the postgres database running in separate container. To successfully start this application you need to have a running postgres database (for instance in docker container).
<br/><br/>

There are two supported ways to start the application:
<br/><br/>

Start the app without the docker
- is quite complicated as it is part of federation API, prefer use in docker
- you need to have running postgres database which is ready to use
- change the ComposeConnectionString inner constants in DBDefinition.py to your postgres address (see used pattern)
- to start the app outside of docker use the following command:
uvicorn main:app --reload
- after application startup you can access the graphQL UI on ip given by uvicorn - remember to add /gql (example: http://127.0.0.1:8000/gql)
- by default the app creates some random database after every startup (not all tables are populated with data)
<br/><br/>

Start the app inside the docker using docker-compose.yml (recommended)
- to start the app as a docker container you first need to create the gql_core image - to do this use following command:
docker build -t gql_core .
- this image contains our solution with SQLAlchemy models and GraphQL endpoint
- (optional) you can run the container standalone on any port you want by using: docker run -p your_port:8001 gql_core
- use docker-compose.yml file to set up postgres database and gql_core using this command:
docker-compose up
- docker will use given compose file to create two containers (isdatabase_gql_entry_point and isdatabase_database)
- gql_entry_point is based on the gql_core image and provides the GraphQL endpoint (contains all our code)
- database container is based on postgres 13.2 image and provides a database (image will be downloaded if necessary)
- postgres is automatically set up by docker-compose.yml - there you can edit variables such as database name, username and password - these will be used by gql to acess the database
- these two containers are able to exchange data between each other on closed docker network
- only gql endpoint is available for other device outside of docker network - to access the GraphQL UI open http://localhost:82/gql on your device
<br/><br/>

- in this version of our project the database is populated with random data (not all databse is populated - for testing purposes only)
<br/><br/>

pytest --cov-report term-missing --cov=gql_granting tests
