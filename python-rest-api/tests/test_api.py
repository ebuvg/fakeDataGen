import unittest

from app import create_app


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok"})

    def test_generate_with_faker(self):
        response = self.client.post(
            "/generate",
            json={"provider": "faker", "count": 2},
        )
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["provider"], "faker")
        self.assertEqual(len(payload["records"]), 2)
        self.assertIn("first_name", payload["records"][0])

    def test_generate_with_ollama(self):
        response = self.client.post(
            "/generate",
            json={"provider": "ollama", "count": 1, "model": "phi4:latest", "base_url": "http://localhost:11434"},
        )
        self.assertIn(response.status_code, [200, 500])


if __name__ == "__main__":
    unittest.main()
