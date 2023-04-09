import json
import logging

import database_operations
import movie_fetcher
import pymongo
from config import MovieManagerSettings
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Get the app settings
settings = MovieManagerSettings()

logging.basicConfig(level=settings.loglevel)

logging.info(f"Starting movie manager with settings: {settings.dict()}")

# Get the database connection, database and movies collection.
connection, movie_database, movies = database_operations.get_db(
    settings.mongo_uri, settings.reset_db
)

logging.info("Connected to database")

app = FastAPI()

logging.info("Starting movie fetcher")
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


@app.get("/api/search")
def name_search(
    search_term: str = None, filters: str = None, order: bool = True
) -> list[dict[str, str]]:
    """
    Search for movies by name and by given filters.

    Args:
        search_term: string to search for in movie name
        filters: json string with filters to apply to the search
        order: True for ascending, False for descending

    Returns:
        Returns list of dicts with keys 'name' and 'image'.
    """

    # set ordering
    ordering = pymongo.ASCENDING if order else pymongo.DESCENDING

    # build filter query
    parsed_filters = {} if not filters else json.loads(filters)

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
def provide_filters() -> dict[str, list[str]]:
    """
    Returns dict of unique values for selected fields in mongoDB collection.

    Args:
        None

    Returns:
        Dict with search fields as keys and list of unique values for given key as values.

    """

    # fields which I want to filter by on frontend
    fields = ["features", "source", "drm"]

    return {field: movies.distinct(field) for field in fields}


@app.get("/api/moviedetail")
def movie_detail(movie_name: str) -> dict[str, str]:
    """
    Returns movie details for a given movie name.

    Args:
        movie_name: name of the movie to get details for

    Returns:
        Dict with movie details.

    """

    querry_result = movies.find_one({"name": movie_name})

    if querry_result is not None:
        result = dict(querry_result)
        del result["_id"]
    else:
        result = {"detail": "Movie not found"}

    return result


# Static files should be provided by nginx in production.
# Apparently if you mount static to root it will override the other routes.
# So I had to put it here.
app.mount("/", StaticFiles(directory="static/", html=True), name="static")
