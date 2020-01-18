from save_the_giphies.libraries.retriever import Retriever
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
        mm.read.return_value = b'{"data": [{"rating": "g"}]}'
        mm.__enter__.return_value = mm
        mock_urlopen.return_value = mm
        payload = Retriever().retrieve_giphies("foo", limit=1)
        self.assertTrue(payload == [{"rating": "g"}])
