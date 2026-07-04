
# Python environment
```
python3 -m venv .venv
On Linux/macOS:     source .venv/bin/activate
Deactivate:         deactivate

pip install package_name
pip install -r requirement.txt
```
# Calling function to generate fake data 
```
python main.py                    # Generate 5 records in JSON format
python main.py -c 10              # Generate 10 records
python main.py -c 3 -o pretty     # Generate 3 records in pretty format
python main.py --help             # See all options

    
# Generate 5 records using Ollama, output as CSV
python main.py --ollama -c 5 -o csv

# Generate 10 records using Ollama in JSON format
python main.py --ollama -c 10

# Generate with custom model and URL
python main.py --ollama -c 5 -o csv --model phi4:latest --ollama-url http://localhost:11434

# Still works with Faker (default)
python main.py -c 5 -o csv
```

# Questions
===========
1- how do you setup a virtual environment in Python?
2- i would like to scaffold a basic application, that runs when i call main.py
3- how do i extract the FakeDataGenerator class into it's own file and call it main.py, using python best pratices.
