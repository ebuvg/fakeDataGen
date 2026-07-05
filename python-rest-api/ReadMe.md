# Python REST API for Fake Data Generation

This folder contains a small Flask REST API that uses the existing fake data generators.

## Features
- Generate fake data with Faker via POST /generate
- Generate fake data with Ollama via POST /generate
- Return responses as JSON
- Provide health and error handling endpoints
- Read data from the existing SQLite database at the project root
- Use a dedicated services folder for reusable API logic

## Setup
```bash
cd python-rest-api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the API
```bash
python app.py
```

The API will be available at:
- http://127.0.0.1:5000/
- http://127.0.0.1:5000/health

## Example requests

### Health check
```bash
curl http://127.0.0.1:5000/health
```

### Read rows from your existing database
```bash
curl http://127.0.0.1:5000/database
```

Example response:
```json
{
  "database": "fakedata.db",
  "records": [
    {
      "field1": "value1",
      "field2": "value2",
      "field3": "value3",
      "field4": "value4",
      "field5": "value5",
      "field6": "value6"
    }
  ]
}
```

### Generate fake data with Faker
```bash
curl -X POST http://127.0.0.1:5000/generate \
  -H "Content-Type: application/json" \
  -d '{"provider": "faker", "count": 2}'
```

Example response:
```json
{
  "provider": "faker",
  "count": 2,
  "records": [
    {
      "first_name": "Jane",
      "last_name": "Doe",
      "email": "jane@example.com",
      "phone": "555-0100",
      "address": "123 Main St",
      "company": "Acme Corp"
    }
  ]
}
```

### Generate fake data with Ollama
```bash
curl -X POST http://127.0.0.1:5000/generate \
  -H "Content-Type: application/json" \
  -d '{"provider": "ollama", "count": 1, "model": "phi4:latest", "base_url": "http://localhost:11434"}'
```

### Invalid request example
```bash
curl -X POST http://127.0.0.1:5000/generate \
  -H "Content-Type: application/json" \
  -d '{"provider": "faker", "count": 0}'
```

Example error response:
```json
{
  "error": "count must be a positive integer"
}
```
