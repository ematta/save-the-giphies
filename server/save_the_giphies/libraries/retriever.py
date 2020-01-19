from urllib.request import urlopen
from save_the_giphies.config import config
import json
from typing import Dict, TYPE_CHECKING, List
from save_the_giphies.libraries.logger import logger

if TYPE_CHECKING:
    from http.client import HTTPResponse


class Retriever:
    """ Main API interface for GIPHY """

    def url(self, endpoint: "str") -> "str":
        """ Builds URL
        Params:
            endpoint (str): The endpoint we want to execute against

        Returns str
        """
        host: "str" = "/".join([config.giphy_host, config.giphy_version, endpoint])
        full_url: "str" = f"{config.giphy_schema}://{host}"
        logger.info(f"URL is {full_url}")
        return full_url

    def retrieve_giphy(self, giphy_id: "str") -> "Dict":
        """Returns the response from Giphy for a single gif
        Parameters:
            giphy_id (str): The giphy id we are dealing with

        Returns Dict
        """
        giphy_id = giphy_id.strip().replace(' ', '%20')
        url: "str" = self.url(config.giphy_gifs_endpoint)
        host: "str" = f"{url}/{giphy_id}?api_key={config.giphy_api_key}"
        res: "HTTPResponse" = urlopen(host)
        body: "bytes" = res.read()
        payload: "Dict" = json.loads(body.decode("utf-8"))
        return payload

    def retrieve_giphies(
        self,
        q: "str",
        limit: "int" = 25,
        offset: "int" = 0,
        rating: "str" = "G",
        lang: "str" = "en",
    ) -> "List[Dict]":
        """Returns the response from Giphy based on a query

        Parameters:
            query (str): The query you want to send
            limit (int): How many you want returned (default: 25)
            offset (int): ... (default: 0)
            rating (str): The rating of the gif you want to see (default: G)
            lang (str): The language you want to see for giphs (default: en)

        Returns List[Dict]
        """
        url: "str" = self.url(config.giphy_search_endpoint)
        q = q.strip().replace(' ', '%20')
        query: "str" = "&".join(
            [
                f"api_key={config.giphy_api_key}",
                f"q={q}",
                f"limit={limit}",
                f"offset={offset}",
                f"rating={rating}",
                f"lang={lang}",
            ]
        )
        url = f"{url}?{query}"
        res: "HTTPResponse" = urlopen(url)
        body: "bytes" = res.read()
        payload: "List[Dict]" = json.loads(body.decode("utf-8"))
        results: "List[Dict]" = [load for load in payload["data"] if load["rating"].lower() == "g"]  # type: ignore
        if len(results) < limit:
            new_limit: "int" = limit - len(results)
            new_offset: "int" = offset + new_limit
            new_results: "List[Dict]" = self.retrieve_giphies(
                q=q, limit=new_limit, offset=new_offset, rating=rating, lang=lang
            )
            results = results + new_results
        return results


retriever = Retriever()
