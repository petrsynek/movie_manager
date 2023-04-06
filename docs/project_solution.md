# Solution

## Tools

### Framework

- [x] **FastAPI** - simple and reliable, not ideal for rendering view - but this project can be done with one template + js
- **Flask** - no advantages
- **Django** - simple but overkill

### Database

- **Elasticsearch** - document based, good for search
- [x] **MongoDB** - document based, still fine for fulltext in movie title
- **Postgres** - could be done using HStoreField or JsonB but there are no relations - no need
- **neo4j** - no relations - no need

### Deployment

- **Local with makefile** - what about mongo? still the app could be run localy?
- [x] **Docker-compose** - should be fine, maybe overkill

## Primary Goals

- setup project with db and server
- cron job that will update data from remote api to db
- serve base page with paginated results
- api endpoint for basic name search that will serve results with custom orderning (asc, desc)

## Secondary Goals

- partial text search
- implement advanced filters bar on page