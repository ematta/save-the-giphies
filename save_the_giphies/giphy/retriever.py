from urllib.request import urlopen
from save_the_giphies.config import config
import json


class Retriever:
    def search_url(self):
        """Returns the URL for giphy search
        """
        url = "/".join(
            [config.giphy_host, config.giphy_version, config.giphy_search_endpoint]
        )
        return f"{config.giphy_schema}://{url}"

    def search_query(
        self,
        query: str,
        limit: int = 25,
        offset: int = 0,
        rating: str = "G",
        lang: str = "en",
    ):
        """Returns the query string for your request

        Parameters:
            query (str): The query you want to send
            limit (int): How many you want returned (default: 25)
            offset (int): ... (default: 0)
            rating (str): The rating of the gif you want to see (default: G)
            lang (str): The language you want to see for giphs (default: en)
        """
        return "&".join(
            [
                f"api_key={config.giphy_api_key}",
                f"q={query}",
                f"limit={limit}",
                f"offset={offset}",
                f"rating={rating}",
                f"lang={lang}",
            ]
        )

    def retrieve_giphies(self, query: str):
        """Returns the response from Giphy based on a query

        Parameters:
            query (str): The query you are sending

        Returns:
            Dict: The json payload from giphy
        """
        res = urlopen(f"{self.search_url()}?{self.search_query(query = query)}")
        body = res.read()
        payload = json.loads(body.decode("utf-8"))
        return payload
