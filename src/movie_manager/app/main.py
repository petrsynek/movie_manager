import json
import logging

import database_operations
import movie_fetcher
import pymongo
from config import MovieManagerSettings
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# Get the app settings
settings = MovieManagerSettings()

logging.basicConfig(level=settings.loglevel)

# Get the database connection, database and movies collection.
connection, movie_database, movies = database_operations.get_db(settings.mongo_uri)

logging.info(settings)

app = FastAPI()

# Start the database updater
movie_fetcher_task = movie_fetcher.run(
    poll_interval=settings.remote_api_poll_interval,
    poll_url=settings.remote_api_url,
    collection=movies,
)


@app.on_event("shutdown")
def shutdown_event():
    """Close the database connection and correctly terminate task on shutdown."""
    movie_fetcher_task.cancel()
    connection.close()


@app.get("/")
def read_root():
    """Serve the frontend page, should be done by nginx in production."""

    with open("frontend/page.html", "r") as f:
        html_content = f.read()

    return HTMLResponse(content=html_content, status_code=200)


@app.get("/api/search")
def name_search(search_term: str, filters: str, order: bool = True):
    """Search for movies by name."""

    # set ordering
    ordering = pymongo.ASCENDING if order else pymongo.DESCENDING

    # build filter query
    parsed_filters = json.loads(filters)

    filter_query = {key: {"$in": parsed_filters[key]} for key in parsed_filters}

    # search querry
    if not search_term:
        find_querry = {}
    else:
        find_querry = {"name": {"$regex": search_term, "$options": "i"}}

    # final querry
    querry = {**find_querry, **filter_query}

    # fetch data
    data = movies.find(querry).sort("name", ordering)

    return [
        {"name": movie["name"], "image": movie.get("iconUri", None)} for movie in data
    ]


@app.get("/api/searchfields")
def provide_filters():
    """Returns dict of unique values for selected fields in mongoDB collection."""

    # fields which I want to filter by
    fields = ["features", "source", "drm"]

    return {field: movies.distinct(field) for field in fields}
