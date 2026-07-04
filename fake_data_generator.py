"""
Fake Data Generator module.

This module provides the FakeDataGenerator class for generating synthetic data.
"""

from typing import List, Dict, Any
from faker import Faker


class FakeDataGenerator:
    """Generate fake user data for testing and development purposes."""

    def __init__(self, locale: str = "en_US"):
        """
        Initialize the FakeDataGenerator.
        
        Args:
            locale: The locale for generated data (default: "en_US")
        """
        self.faker = Faker(locale)

    def generate_users(self, count: int = 5) -> List[Dict[str, Any]]:
        """
        Generate fake user records.
        
        Args:
            count: Number of fake user records to generate
            
        Returns:
            List of dictionaries containing user data
        """
        if count < 1:
            raise ValueError("Count must be at least 1")
        
        data = []
        for _ in range(count):
            record = {
                "name": self.faker.name(),
                "email": self.faker.email(),
                "phone": self.faker.phone_number(),
                "address": self.faker.address(),
                "company": self.faker.company(),
            }
            data.append(record)
        
        return data
