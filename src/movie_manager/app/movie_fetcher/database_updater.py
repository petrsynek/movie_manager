import asyncio
import json
import urllib.request
from logging import getLogger
from typing import Callable

from pymongo.collection import Collection

logger = getLogger(__name__)


async def schedule_job(interval: int, job: Callable, *args, **kwargs) -> None:
    while True:
        await job(*args, **kwargs)
        await asyncio.sleep(interval)


async def download_data_from_api_and_update_database(
    url: str, collection: Collection
) -> None:
    response = urllib.request.urlopen(url)
    movies_data = json.loads(response.read())
    logger.info("Updating database")
    for movie in movies_data:
        collection.update_one({"name": movie["name"]}, {"$set": movie}, upsert=True)


def run(collection: Collection) -> asyncio.Task:
    task = asyncio.create_task(
        schedule_job(
            1,
            download_data_from_api_and_update_database,
            "https://gist.githubusercontent.com/nextsux/f6e0327857c88caedd2dab13affb72c1/raw/04441487d90a0a05831835413f5942d58026d321/videos.json",  # noqa: E501
            collection,
        )
    )
    return task
