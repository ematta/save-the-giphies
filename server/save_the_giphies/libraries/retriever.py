from urllib.request import urlopen
from save_the_giphies.config import config
import json


class Retriever:
    def url(self):
        host = "/".join(
            [config.giphy_host, config.giphy_version, config.giphy_search_endpoint]
        )
        return f"{config.giphy_schema}://{host}"

    def retrieve_giphy(self, giphy_id: str):
        """Returns the response from Giphy for a single gif
        Parameters:
            giphy_id (str): The giphy id we are dealing with

        Returns:
            Dict: The json payload from giphy
        """
        url: str = f"{url}/gifs/{giphy_id}"
        res  = urlopen(url)
        body = res.read()
        payload = json.loads(body.decode("utf-8"))
        return payload

    def retrieve_giphies(
        self,
        q: str,
        limit: int = 25,
        offset: int = 0,
        rating: str = "G",
        lang: str = "en",
    ):
        """Returns the response from Giphy based on a query

        Parameters:
            query (str): The query you want to send
            limit (int): How many you want returned (default: 25)
            offset (int): ... (default: 0)
            rating (str): The rating of the gif you want to see (default: G)
            lang (str): The language you want to see for giphs (default: en)

        Returns:
            Dict: The json payload from giphy
        """
        url = "/".join(
            [config.giphy_host, config.giphy_version, config.giphy_search_endpoint]
        )
        query = "&".join(
            [
                f"api_key={config.giphy_api_key}",
                f"q={q}",
                f"limit={limit}",
                f"offset={offset}",
                f"rating={rating}",
                f"lang={lang}",
            ]
        )
        url = f"{config.giphy_schema}://{url}?{query}"
        res = urlopen(url)
        body = res.read()
        payload = json.loads(body.decode("utf-8"))
        return payload


retriever = Retriever()
