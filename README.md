# Flask with PostgreSQL and OpenAI Integration

This project demonstrates a Flask application integrated with PostgreSQL and OpenAI's API. The application allows users to ask questions, get answers from OpenAI, and store the questions and answers in a PostgreSQL database.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Running Tests](#running-tests)
- [Project Structure](#project-structure)
- [License](#license)

## Features

- Ask questions via a POST endpoint and get responses from OpenAI.
- Store questions and answers in a PostgreSQL database.

## Requirements

- Docker
- Docker Compose
- Python 3.10
- OpenAI API key

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/yourusername/flask-postgres-openai.git
   cd flask-postgres-openai```
2. **Set up environment variables:**
Open the .env.example file and add your OpenAI API key.
After you are done, don't forget to change the name of the file to .env .

3. **Build and run the Docker containers:**
Using the terminal, go to the project directory and then run the docker-compose up command (it will take a few seconds because of the health checks):

```sh
docker-compose up --build
```

## Usage

Send a POST request to the /ask endpoint with a JSON payload containing the question:

```sh
curl -X POST http://localhost:5000/ask \
    -H "Content-Type: application/json" \
    -d '{"question": "What is the capital of France?"}'
```
## Running Tests

1. **Install pytest:**

Make sure pytest and requests is installed in your environment:

```sh
pip install pytest
pip install requests
```

2. **Run the tests:**

Navigate to the tests folder from your terminal and then run:

```sh
pytest test_app.py
```

## Project Structure ##

```
.
├── alembic/
│   └── first commit
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
├── tests/
│   └── test_app.py
├── .env.example
├── .gitignore
├── Dockerfile
├── Dockerfile.db
├── README.md
├── alembic.ini
├── app.py
├── docker-compose.yml
├── pg_hba.conf
├── postgresql.conf
├── requirements.txt

```

- **alembic/**: Contains database migration scripts.
- **app/**: Contains the Flask application code.
    - **__init__.py**: Initializes the Flask app and sets up the database.
    - **models.py**: Defines the database models.
    - **routes.py**: Defines the application routes and logic.
- **tests/**: Contains the test files.
    - **test_app.py**: Contains the tests for the Flask application.
- **.env.example**: Example environment variables file.
- **.gitignore**: Specifies files and directories to be ignored by git.
- **Dockerfile**: Defines the Docker image for the Flask app.
- **Dockerfile.db**: Defines the Docker image for the PostgreSQL database.
- **README.md**: This readme file.
- **alembic.ini**: Alembic configuration file for database migrations.
- **app.py**: Entry point for the Flask application.
- **docker-compose.yml**: Configures the Docker services.
- **pg_hba.conf**: PostgreSQL client authentication configuration file.
- **postgresql.conf**: Custom PostgreSQL configuration file.
- **requirements.txt**: Python dependencies.


## License ##

This project is licensed under the MIT License.
