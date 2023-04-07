import logging

import database_operations
import movie_fetcher
from fastapi import FastAPI

app = FastAPI()

logging.basicConfig(level=logging.DEBUG)

connection, movie_database, movies = database_operations.get_db()

movie_fetcher.run(movies)


@app.get("/")
def read_root():
    data = movies.find({})
    repsonse = [movie["name"] for movie in data]
    return {"entries": len(repsonse), "movies": repsonse}


@app.get("/search/{search_term}")
def name_search(search_term: str):
    data = movies.find({"$text": {"$search": search_term}})
    repsonse = [movie["name"] for movie in data]
    return {"entries": len(repsonse), "movies": repsonse}
