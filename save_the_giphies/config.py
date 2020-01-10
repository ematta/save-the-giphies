from dataclasses import dataclass
from typing import Optional
import os


@dataclass
class Config:
    giphy_schema: str = "https"
    giphy_host: str = "api.giphy.com"
    giphy_version: Optional[str] = os.getenv("GIPHY_API_VERSION", "v1")
    giphy_search_endpoint: str = "gifs/search"
    giphy_api_key: Optional[str] = os.getenv("GIPHY_API_KEY")
    debug: Optional[bool] = bool(os.getenv("DEBUG"))


config = Config()
