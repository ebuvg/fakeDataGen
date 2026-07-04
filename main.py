#!/usr/bin/env python3
"""
Fake Data Generator - A CLI application to generate synthetic data.
"""

import argparse
import csv
import json
import sys

from fake_data_generator import FakeDataGenerator
from ollama_generator import OllamaDataGenerator, OllamaModelError


def format_output(data: list, output_format: str) -> None:
    """
    Format and print the generated data.
    
    Args:
        data: List of data records to display
        output_format: Format for output ("json", "pretty", or "csv")
    """
    if output_format == "csv":
        if not data:
            print("No data to export")
            return
        
        # Get field names from first record
        fieldnames = list(data[0].keys())
        writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
        
    elif output_format == "pretty":
        for i, record in enumerate(data, 1):
            print(f"\n--- Record {i} ---")
            for key, value in record.items():
                print(f"{key}: {value}")
    else:  # json
        print(json.dumps(data, indent=2))


def main() -> None:
    """Main entry point for the CLI application."""
    parser = argparse.ArgumentParser(
        description="Generate fake data for testing purposes"
    )
    parser.add_argument(
        "-c", "--count",
        type=int,
        default=5,
        help="Number of fake records to generate (default: 5)"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="json",
        choices=["json", "pretty", "csv"],
        help="Output format (default: json)"
    )
    parser.add_argument(
        "--ollama",
        action="store_true",
        help="Use Ollama to generate data instead of Faker"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="phi4:latest",
        help="Ollama model to use (default: phi4:latest)"
    )
    parser.add_argument(
        "--ollama-url",
        type=str,
        default="http://localhost:11434",
        help="Ollama server URL (default: http://localhost:11434)"
    )
    parser.add_argument(
        "--pull-model",
        action="store_true",
        help="Pull the requested Ollama model before generating data"
    )
    
    args = parser.parse_args()
    
    try:
        # Generate data
        if args.ollama:
            generator = OllamaDataGenerator(model=args.model, base_url=args.ollama_url)
            if args.pull_model:
                import subprocess
                subprocess.run(["ollama", "pull", args.model], check=True)
            data = generator.generate_records(count=args.count)
        else:
            generator = FakeDataGenerator()
            data = generator.generate_users(count=args.count)
        
        # Display output
        format_output(data, args.output)
        
    except OllamaModelError as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
