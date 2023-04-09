from logging import getLogger
from typing import Tuple

import pymongo
from config import MyMongoDsn

logger = getLogger(__name__)


def get_db(
    db_settings: MyMongoDsn,
    reset: bool = False,
) -> Tuple[
    pymongo.database.Database, pymongo.MongoClient, pymongo.collection.Collection
]:
    """Get a database connection, database and movies collection."""

    logger.info(f"Connecting to database {db_settings.database}")

    client = pymongo.MongoClient(host=db_settings.host, port=db_settings.port)

    # Resets the database if requested.
    if reset:
        logger.info("Resetting database")
        client.drop_database(db_settings.database)

    # select database
    db = client[db_settings.database]

    # setup collection with indexes
    collection = db["movies"]
    collection.create_index("name", unique=True)
    collection.create_index([("name", "text")])

    logger.info("Database setup complete")

    return client, db, collection
