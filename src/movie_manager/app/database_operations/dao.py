from typing import Tuple

import pymongo


def get_db(
    reset: bool = True,
) -> Tuple[
    pymongo.database.Database, pymongo.MongoClient, pymongo.collection.Collection
]:

    client = pymongo.MongoClient(host="mongo", port=27017)

    if reset:
        client.drop_database("movie_database")

    # select database
    db = client["movie_database"]
    collection = db["movies"]
    collection.create_index("name", unique=True)
    collection.create_index([("name", "text")])
    return client, db, collection
