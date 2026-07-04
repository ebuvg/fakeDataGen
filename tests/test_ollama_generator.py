import unittest
from unittest.mock import patch

from ollama_generator import OllamaDataGenerator


class OllamaGeneratorTests(unittest.TestCase):
    def test_missing_model_error_is_user_friendly(self):
        generator = OllamaDataGenerator.__new__(OllamaDataGenerator)
        generator.model = "missing-model"
        generator.base_url = "http://localhost:11434"

        class StubClient:
            def generate(self, **kwargs):
                raise Exception("model 'missing-model' not found")

            def pull(self, model, stream=False):
                return None

        generator.client = StubClient()

        with self.assertRaises(RuntimeError) as context:
            generator._generate_from_prompt("{}")

        self.assertIn("not found", str(context.exception))
        self.assertIn("Install or pull", str(context.exception))


if __name__ == "__main__":
    unittest.main()
