import re
from logging import getLogger
from typing import Optional, Union

from pydantic import BaseModel, BaseSettings, validator

logger = getLogger(__name__)


class MyMongoDsn(BaseModel):
    """
    MongoDB DSN - decided to implement my own because pydantic's
    MongoDsn doesn't support database (just extedns AnyUrl)
    """

    uri: str
    host: str
    port: int
    database: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None

    @classmethod
    def model_dict_from_uri(cls, input_data):
        if isinstance(input_data, str):
            pattern = r"^(mongodb:(?:\/{2})?)((?P<username>\w+?)?:(?P<password>\w+?)?@|:?@?)(?P<host>\w+?):(?P<port>\d+)(\/(?P<database>\w+?))?$"  # noqa: E501
            match = re.search(pattern, input_data)
            if match:
                group_dict = match.groupdict()
                group_dict["uri"] = input_data
                return group_dict

        raise ValueError(f"Invalid URI {input_data}")


class MovieManagerSettings(BaseSettings):
    """
    Movie Manager settings.
    """

    mongo_uri: Union[str, MyMongoDsn] = "mongodb://mongo:27017/movie_database"
    remote_api_url: str
    remote_api_poll_interval: int = 100
    loglevel: str = "DEBUG"
    reset_db: bool = False

    @validator("mongo_uri", pre=True)
    def validate_mongo_uri(cls, input_data):
        if isinstance(input_data, str):
            return MyMongoDsn.model_dict_from_uri(input_data)
        else:
            return input_data

    class Config:
        case_sensitive = False
