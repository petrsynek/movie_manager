# Solution

## Tools

### Framework

- [x] **FastAPI** - simple
- **Flask** - just bad compromise betweent the two
- **Django** - would take care of everything but overkill

### Database

- **Elasticsearch** - document based, good for search
- [x] **MongoDB** - document based, still fine for search in movie title, never worked with - at least I will learn somthing
- **Postgres** - could be done using HStoreField or JsonB but there are no relations which would make relational DB justified
- **neo4j** - no relations - no need

### Deployment

- **Local with makefile** - what about mongo? would require someone to install mongo
- [x] **Docker-compose with makefile** - should be fine as every dev has docker nowdays

## Primary Goals

- [x] setup project with db and server
- [x] cron job that will update data from remote api to db
- [x] serve base page with paginated results
- [x] api endpoint for basic name search 
- [x] provide custom orderning (asc, desc)
- [x] display details on card click
- [x] add tests 

## Secondary Goals

- [x] partial text search
- [x] implement advanced filters bar on page
- [x] make app properly configurable
  
Not going to do as this is too much nice to have for homework:
- [ ] make all nice with db as dependency injection and not global variable
- [ ] move all db operations to dao
- [ ] move routes out of main

## Issues

- the html page layout is not masterwork and the script is even worse but I suppose it's ok for homework for backend developer
- the pagination was not required and as now is delegated to front end would cause problems on db as there is currently no limit on query, lets say this does not scale nicely with large db, could be easily fixed if nescessary
- also because I like the look of it, I dont perform text search (on whole words) but regex search, which would likely to fry the db in real production (but looks super cool anyway)
- api tested by tests, frontend tested manualy, as this is homework I am not going to setup selenium tests for this