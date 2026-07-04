"""
Ollama-based Fake Data Generator module.

This module provides the OllamaDataGenerator class for generating synthetic data
using Ollama language models.
"""

import json
from typing import List, Dict, Any

try:
    import ollama
except ImportError:
    ollama = None


class OllamaModelError(RuntimeError):
    """Raised when the requested Ollama model is unavailable."""



class OllamaDataGenerator:
    """Generate fake data using Ollama language models."""

    def __init__(self, model: str = "phi4:latest", base_url: str = "http://localhost:11434"):
        """
        Initialize the OllamaDataGenerator.
        
        Args:
            model: The Ollama model to use (default: "phi4:latest")
            base_url: The base URL of the Ollama server (default: "http://localhost:11434")
            
        Raises:
            ImportError: If ollama package is not installed
        """
        if ollama is None:
            raise ImportError("ollama package not installed. Run: pip install ollama")
        
        self.model = model
        self.base_url = base_url
        self.client = ollama.Client(host=base_url)

    def _generate_from_prompt(self, prompt: str) -> List[Dict[str, Any]]:
        """Generate records from a prompt and parse the response JSON."""
        try:
            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                stream=False,
            )
        except Exception as exc:
            message = str(exc)
            if "not found" in message.lower() or "404" in message:
                try:
                    self.client.pull(self.model, stream=False)
                except Exception as pull_exc:
                    raise OllamaModelError(
                        f"Model '{self.model}' was not found on {self.base_url}. "
                        f"Install or pull it first, for example: ollama pull {self.model}. "
                        f"Pull attempt failed: {pull_exc}"
                    ) from pull_exc

                try:
                    response = self.client.generate(
                        model=self.model,
                        prompt=prompt,
                        stream=False,
                    )
                except Exception as retry_exc:
                    raise OllamaModelError(
                        f"Model '{self.model}' was not found on {self.base_url}. "
                        f"Install or pull it first, for example: ollama pull {self.model}. "
                        f"Retry failed: {retry_exc}"
                    ) from retry_exc
            else:
                raise RuntimeError(f"Ollama generation failed: {message}") from exc

        response_text = response.get("response", "").strip()

        start_idx = response_text.find("[")
        end_idx = response_text.rfind("]") + 1

        if start_idx != -1 and end_idx > start_idx:
            json_str = response_text[start_idx:end_idx]
            data = json.loads(json_str)
            if isinstance(data, list):
                return data

        raise ValueError("Failed to parse valid JSON from Ollama response")

    def generate_records(self, count: int = 5, fields: List[str] = None) -> List[Dict[str, Any]]:
        """
        Generate fake data records using Ollama.
        
        Args:
            count: Number of fake records to generate
            fields: List of fields to include (default: name, email, phone, address, company)
            
        Returns:
            List of dictionaries containing generated data
            
        Raises:
            ValueError: If count is less than 1
        """
        if count < 1:
            raise ValueError("Count must be at least 1")
        
        if fields is None:
            fields = ["name", "email", "phone", "address", "company"]

        prompt = f"""Generate {count} fake user records in valid JSON format with the following fields: {', '.join(fields)}.
        
Return ONLY valid JSON array with no additional text or markdown formatting. Example format:
[{{"name": "John Doe", "email": "john@example.com", "phone": "555-0100", "address": "123 Main St", "company": "Acme Corp"}}]

Generate the data now:"""

        try:
            return self._generate_from_prompt(prompt)
        except OllamaModelError:
            raise
        except Exception as e:
            raise RuntimeError(f"Ollama generation failed: {str(e)}") from e
