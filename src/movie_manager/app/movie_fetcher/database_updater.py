import asyncio
import json
from logging import getLogger
from typing import Callable

import aiohttp
from pydantic import AnyUrl
from pymongo.collection import Collection

logger = getLogger(__name__)


async def schedule_job(interval: int, job: Callable, *args, **kwargs) -> None:
    """Schedule a job to run every 'interval' seconds."""
    while True:
        await job(*args, **kwargs)
        await asyncio.sleep(interval)


async def download_data_from_api_and_update_database(
    url: str, collection: Collection
) -> None:
    """
    Download data from API and update database.
    If movie is not in database, add it. If it is, update it.
    """

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                movies_data = await resp.text()

    except aiohttp.web.HTTPException as e:
        logger.error(f"Error downloading data from API: {e}")
        return

    movies_data = json.loads(movies_data)

    logger.info("Updating database")
    for movie in movies_data:
        collection.update_one({"name": movie["name"]}, {"$set": movie}, upsert=True)


def run(poll_interval: int, poll_url: AnyUrl, collection: Collection) -> asyncio.Task:
    """Run the database updater."""
    task = asyncio.create_task(
        schedule_job(
            poll_interval,
            download_data_from_api_and_update_database,
            poll_url,
            collection,
        )
    )
    return task
