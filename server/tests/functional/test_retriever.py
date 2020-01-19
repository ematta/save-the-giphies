from save_the_giphies.libraries.retriever import Retriever  # type: ignore
import unittest


class TestRetriever(unittest.TestCase):
    def setUp(self):
        self.retriever = Retriever()

    def tearDown(self):
        self.retriever = None

    def test_get_retriever(self):
        res = self.retriever.retrieve_giphies(q="test")
        self.assertTrue(len(res) > 0)
        for data in res:
            self.assertTrue(data["rating"] == "g")

    def test_single_giphy(self):
        test_id = "xT4uQulxzV39haRFjG"
        payload = self.retriever.retrieve_giphy(test_id)
        self.assertIsInstance(payload, dict)
        self.assertIn(payload["data"]["id"], test_id)
        self.assertTrue(payload["data"]["rating"] == "pg")
