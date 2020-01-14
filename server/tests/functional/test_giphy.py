import unittest
import json
from save_the_giphies.app import app


class TestGiphy(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["DEBUG"] = False
        self.app = app.test_client()

    def test_search(self):
        response = self.app.post(
            "/giphy/search",
            json={"q": "test"},
            headers={"Accept": "application/json"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode("utf-8"))["data"]
        self.assertTrue(len(data) == 25)
        self.assertTrue(data[0]["rating"] == "g")

    def test_search_limit(self):
        response = self.app.post(
            "/giphy/search",
            json={"q": "test", "limit": 100},
            headers={"Accept": "application/json"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode("utf-8"))["data"]
        self.assertTrue(len(data) == 100)
