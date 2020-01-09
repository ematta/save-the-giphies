from save_the_giphies.giphy.retriever import Retriever  # type: ignore
import unittest


class TestRetriever(unittest.TestCase):
    def setUp(self):
        self.retriever = Retriever()

    def tearDown(self):
        self.retriever = None

    def test_get_retriever(self):
        res = self.retriever.retrieve_giphies(query="test")
        self.assertTrue(len(res) > 0)
        for data in res["data"]:
            self.assertTrue(data["rating"] == "g")
