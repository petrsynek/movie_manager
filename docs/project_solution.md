# Solution

## Tools

### Framework

- [x] **FastAPI** - simple and reliable, not ideal for rendering view - but this project can be done with one template + js
- **Flask** - no advantages
- **Django** - simple but overkill

### Database

- **Elasticsearch** - document based, good for search
- [x] **MongoDB** - document based, still fine for fulltext in movie title, never worked with - at least I will learnd smthing
- **Postgres** - could be done using HStoreField or JsonB but there are no relations - no need
- **neo4j** - no relations - no need

### Deployment

- **Local with makefile** - what about mongo? still the app could be run localy?
- [x] **Docker-compose** - should be fine, maybe overkill

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