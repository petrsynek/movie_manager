import logging

import database_operations
import movie_fetcher
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
movie_fetcher.run(
    poll_interval=settings.remote_api_poll_interval,
    poll_url=settings.remote_api_url,
    collection=movies,
)


@app.get("/")
def read_root():
    """Serve the frontend page."""
    with open("frontend/page.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/api/search")
def name_search(search_term: str):
    """Search for movies by name."""

    if not search_term:
        data = movies.find({})
    else:
        data = movies.find({"name": {"$regex": search_term, "$options": "i"}})

    repsonse = []
    for movie in data:
        image = movie.get("iconUri", None)
        repsonse.append({"name": movie["name"], "image": image})
    return repsonse
