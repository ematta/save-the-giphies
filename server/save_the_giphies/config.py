from dataclasses import dataclass
from typing import Optional
import os


@dataclass
class Config:
    giphy_schema: str = "https"
    giphy_host: str = "api.giphy.com"
    giphy_version: str = os.getenv("GIPHY_API_VERSION", "v1")
    giphy_search_endpoint: str = "gifs/search"
    giphy_gifs_endpoint: str = "gifs"
    giphy_api_key: Optional[str] = os.getenv("GIPHY_API_KEY")
    debug: Optional[bool] = bool(os.getenv("DEBUG"))
    database_url: str = os.environ["POSTGRES_URL"]
    database_port: str = os.environ["POSTGRES_PORT"]
    database_user: str = os.environ["POSTGRES_USER"]
    database_password: str = os.environ["POSTGRES_PASSWORD"]
    database_schema: str = os.environ["POSTGRES_DB"]
    secret_key: str = os.environ["SECRET_KEY"]


config = Config()
