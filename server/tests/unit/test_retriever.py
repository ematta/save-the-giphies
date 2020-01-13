from save_the_giphies.libraries.retriever import Retriever
from save_the_giphies.config import config
import unittest
from unittest.mock import patch, MagicMock


class TestRetriever(unittest.TestCase):
    def setUp(self):
        self.retriever = Retriever()

    def tearDown(self):
        self.retriever = None

    @patch("save_the_giphies.libraries.retriever.urlopen")
    def test_retrieve_giphies(self, mock_urlopen):
        mm = MagicMock()
        mm.getcode.return_value = 200
        mm.read.return_value = b'{"foo": "bar"}'
        mm.__enter__.return_value = mm
        mock_urlopen.return_value = mm
        payload = Retriever().retrieve_giphies("foo")
        self.assertTrue(payload == {"foo": "bar"})

    def test_search_url(self):
        url = self.retriever.search_url()
        self.assertTrue(url.startswith(config.giphy_schema))
        self.assertTrue(url.endswith(config.giphy_search_endpoint))
        self.assertIn(config.giphy_host, url)
        self.assertIn(config.giphy_version, url)

    def test_search_query(self):
        query = "foo"
        query_string = self.retriever.search_query(query)
        self.assertIn(f"api_key={config.giphy_api_key}", query_string)
        self.assertIn(f"q={query}", query_string)
        self.assertIn("limit=25", query_string)
        self.assertIn("offset=0", query_string)
        self.assertIn("rating=G", query_string)
        self.assertIn("lang=en", query_string)
