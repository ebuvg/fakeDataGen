
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
python main.py -c 3 -o csv        # Generate 3 records in csv format
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

# REST API
Run the API locally with:
```
python api.py
```
Then open:
```
http://127.0.0.1:5000/health
http://127.0.0.1:5000/generate?count=3
```

# key notes
```
- pip list shows installed packages in a readable table.
- pip freeze shows packages in requirements.txt format (package==version), making it useful for reproducible environments.

$ pip freeze
annotated-types==0.7.0
anyio==4.14.1
certifi==2026.6.17
Faker==24.1.0
h11==0.16.0
httpcore==1.0.9
httpx==0.28.1
idna==3.18
ollama==0.6.2
pydantic==2.13.4
pydantic_core==2.46.4
python-dateutil==2.9.0.post0
six==1.17.0
typing-inspection==0.4.2
typing_extensions==4.15.0
-------------------------------------------------------------
1)
# git add .gitignore
# git commit -m "add git ignore file"

2)
# git rm -r --cached .venv
# git commit -m "remove .venv from tracking"

```
# Questions
===========
1- how do you setup a virtual environment in Python?
2- i would like to scaffold a basic application, that runs when i call main.py
3- how do i extract the FakeDataGenerator class into it's own file and call it main.py, using python best pratices.
4- I would like to connect to my Ollama server. I want to use the "phi:lates" model. I would like to send a prompt to it asking for fake data and have it return in a CSV format.

5- I would like to create a web API that use rest. 
5- i would like to create a web api is python-rest-api with my existing file. I  would like to accept REST commands
