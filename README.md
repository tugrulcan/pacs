# Floy Tech Challenge

System mock for managing medical transactions.

---
## Project Structure

This README section outlines the structure of the project, detailing each key directory and its contents.

### `automation_pac_client`

- **Purpose**: This directory is dedicated to browser automation codes used for uploading files into Orthanc PACS. The primary goal is to populate the PACS with data for development and manual testing purposes.
- **Contents**: It contains automation scripts developed using Playwright. These scripts streamline the operations outlined in the "Filling the PACS with data and using it" section, thereby automating them for efficiency and consistency.

### `floy`

- **Purpose**: The `floy` directory is the core of the API implementation. It serves as the project's backbone, housing essential components for the application's functionality.
- **Contents**: This directory encompasses the API implementation details, including Database (DB) models, services, and routers. The structure is designed to be scalable and flexible, providing a robust base for project expansion and further development.

### `pac_client`

- **Purpose**: This directory originated from the technical challenge code provided in the initial phase of the project. It forms a crucial part of the application's foundational code.
- **Contents**: In this section, the original classes have been renamed and reorganized into separate files. Although the changes are minor, they are significant for improving code readability and maintainability. The restructuring facilitates easier navigation and understanding of the codebase.

---
## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Development

* Requirements:
  * [Poetry 1.4.0](https://python-poetry.org/)
  * Python 3.10+


* Create a virtual environment and install the dependencies

    ```sh
    poetry install
    ```

* Activate the virtual environment

    ```sh
    poetry shell
    ```

* [Optional] Setup Pycharm to use poetry environment using [Pycharm Python environment setup guide](https://www.jetbrains.com/help/pycharm/poetry.html)


### Pre-commit
Pre-commit hooks run all the auto-formatters (e.g. black, isort), linters (e.g. mypy, flake8), and other quality checks
* Install pre-commit hooks
  * Prerequisites
  * [pre-commit 3.2.0+](https://pre-commit.com/#install)

    ```bash
    pre-commit install
    ```

- Note: **The settings for the pre-commit configured to run unit tests on pre-push stage**. In order to install hooks on pre-push, run the following command:
    ```bash
    pre-commit install --hook-type pre-push
    ```

-  Run linters, type checks and code quality checks
    ```sh
    pre-commit run --all-files
    ```
## Pre-commit Hooks
<details>
  <summary>Click to view pre-commit hooks table</summary>

| Hook ID                        | Description                                                                                          |
|--------------------------------|------------------------------------------------------------------------------------------------------|
| `check-useless-excludes`       | Checks for useless exclusions in pre-commit configuration.                                           |
| `check-poetry`                 | Ensures Poetry files are valid and formatted correctly.                                              |
| `hadolint-docker`              | Lint Dockerfiles using Hadolint.                                                                     |
| `python-no-log-warn`           | Checks for the deprecated `log.warn` in Python files.                                                 |
| `python-no-eval`               | Checks for usage of `eval` in Python files.                                                          |
| `python-use-type-annotations`  | Ensures type annotations are used in Python files.                                                   |
| `rst-backticks`                | Checks for single backticks in RST files (which often should be double).                             |
| `rst-directive-colons`         | Checks for missing colons in RST directive options.                                                  |
| `rst-inline-touching-normal`   | Checks for inline literals touching normal text in RST files.                                        |
| `check-ast`                    | Validates that Python files are syntactically correct.                                               |
| `check-added-large-files`      | Prevents accidentally adding large files to the repository.                                          |
| `check-merge-conflict`         | Checks for unresolved merge conflicts in files.                                                      |
| `check-case-conflict`          | Checks for files that would conflict in case-insensitive filesystems.                                |
| `check-docstring-first`        | Ensures that docstrings are the first thing in Python modules.                                       |
| `check-json`                   | Checks JSON files for syntax errors and formatting issues.                                           |
| `check-yaml`                   | Checks YAML files for syntax and formatting issues.                                                  |
| `check-toml`                   | Checks TOML files for syntax and formatting issues.                                                  |
| `debug-statements`             | Checks for remnants of debug statements (e.g., breakpoints).                                         |
| `end-of-file-fixer`            | Ensures that files end with a newline.                                                               |
| `trailing-whitespace`          | Removes trailing whitespace.                                                                         |
| `mixed-line-ending`            | Checks for mixed line ending styles.                                                                 |
| `check-symlinks`               | Checks for broken symlinks.                                                                          |
| `autoflake`                    | Removes unused imports and variables with Autoflake.                                                 |
| `isort`                        | Sorts Python imports alphabetically and automatically separated into sections.                       |
| `black`                        | Formats Python code to adhere to the Black code style.                                               |
| `pyupgrade`                    | Upgrades Python syntax to newer versions.                                                            |
| `mypy`                         | Runs type checks on Python files.                                                                    |


</details>


## Serving API locally

#### Prerequisites

- Docker and Docker-compose

#### 1. Start the DB, API, Orthanc PACS image, and Automation for PACS client
```sh
docker-compose down -v && docker-compose up
```

#### 2. Visit the API documentation

- When the containers are running double check if the app is being served on your local by visiting this URL:

    [API documentation](http://0.0.0.0:8000/docs)

    It should look like below:
    ![image](https://github.com/tugrulcan/havhav/assets/12617804/5d70d255-9884-47f2-83fe-2bd69fd35ec9)

#### 3. Start the client worker
```sh
poetry run python -m src.pac_client.client
```

## API Documentation
The API documentation is automatically generated from the request and response payload models.
In order to view the documentation, after start running the API locally, and  please visit [API documentation](http://localhost:8001/docs).
---

## Testing

Currently, the project does not include unit tests. This is due to the limited time I had for the overall solution. However, testing is a critical aspect of this project, and the following areas are identified for future unit testing:

### Proposed Unit Tests

- **Models and Validations**:
  - Purpose: To ensure that the models adhere to their defined constraints.
  - Focus: Validate the integrity and constraints of various data models within the application.

- **Database Handler**:
  - Purpose: To verify the correct persistence of data in the database.
  - Focus: Test data storage and retrieval processes to ensure that the database handler is functioning correctly.

- **Services**:
  - Purpose: To confirm that existing data is being updated correctly, rather than creating redundant inserts.
  - Focus: Check the logic within services to ensure they are accurately processing and updating data.

- **API Routers**:
  - Purpose: To validate the proper integration and interaction between the API routers and services.
  - Focus: Ensure that API routers are correctly calling and utilizing the services as intended.

### Additional Testing Considerations

- **`pac_client` Module**:
  - Observation: More comprehensive testing is desired for the `pac_client` module. However, this will require additional refactoring to make the code more testable.
  - Areas for Refactoring:
    - Race conditions while using the Queue.
    - Extracting methods for better modularity and testability.
    - Handling events and scenarios involving incorrect message structures.
  - Goal: Enhance the testability of the `pac_client` module to allow for more thorough testing.

To run the existing tests, use the following command:

```sh
poetry run pytest
```
---


## Dependencies, Frameworks, and Libraries
<details>
  <summary>Click to view dependency table for production</summary>

| Dependency                                              |                                                                                                      Description                                                                                                      |
|---------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| [fastapi](https://github.com/tiangolo/fastapi)          | FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints. |
| [uvicorn](https://www.uvicorn.org/)                     | Uvicorn is an ASGI web server implementation for Python. We use Uvicorn to serve our API. |
| [sqlmodel](https://sqlmodel.tiangolo.com/)              | SQLModel is based on Python type annotations, and powered by Pydantic and SQLAlchemy. |
| [pydantic-settings](https://pydantic-docs.helpmanual.io/) | Data validation and settings management using python type annotations. Pydantic enforces type hints at runtime and provides user-friendly errors when data is invalid. |
| [psycopg2](https://www.psycopg.org/docs/)               | Psycopg is the most popular PostgreSQL database adapter for the Python programming language. |
| [alembic](https://alembic.sqlalchemy.org/en/latest/)    | Alembic is a lightweight database migration tool for usage with the SQLAlchemy Database Toolkit for Python. |

</details>

<details>
  <summary>Click to view dependency table for development</summary>

| Dependency                                              |                                                                                                      Description                                                                                                      |
|---------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| [autoflake](https://github.com/myint/autoflake)         | Autoflake removes unused imports and unused variables from Python code. |
| [black](https://github.com/psf/black)                   | Black is the uncompromising Python code formatter. |
| [flake8](https://flake8.pycqa.org/en/latest/)           | Flake8 is a tool for style guide enforcement and linting. |
| [flake8-bugbear](https://github.com/PyCQA/flake8-bugbear) | A flake8 plugin to find likely bugs and design problems in your program. |
| [flake8-builtins](https://github.com/gforcada/flake8-builtins) | Check for python builtins being used as variables or parameters. |
| [flake8-comprehensions](https://github.com/adamchainz/flake8-comprehensions) | A flake8 plugin to help you write better list/set/dict comprehensions. |
| [flake8-debugger](https://github.com/jbkahn/flake8-debugger) | Flake8 plugin to find and eradicate pdb imports and ipdb statements. |
| [flake8-eradicate](https://github.com/sobolevn/flake8-eradicate) | Flake8 plugin to find commented out or dead code. |
| [flake8-logging-format](https://github.com/globality-corp/flake8-logging-format) | Plugin for flake8 finding logging format issues. |
| [isort](https://github.com/PyCQA/isort)                 | isort is a Python utility / library to sort imports alphabetically and automatically separated into sections. |
| [mypy](http://mypy-lang.org/)                           | Mypy is an optional static type checker for Python. |
| [pep8-naming](https://github.com/PyCQA/pep8-naming)     | Check PEP 8 naming conventions, plugin for flake8. |
| [pre-commit](https://pre-commit.com/)                   | A framework for managing and maintaining multi-language pre-commit hooks. |
| [pytest](https://docs.pytest.org/en/stable/)            | pytest is a framework that makes building simple and scalable test cases easy. |
| [pytest-github-actions-annotate-failures](https://github.com/pytest-dev/pytest-github-actions-annotate-failures) | Plugin for pytest to annotate failures in GitHub actions. |
| [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/) | Pytest plugin for measuring code coverage. |
| [pyupgrade](https://github.com/asottile/pyupgrade)      | A tool to automatically upgrade syntax for newer versions of the language. |
| [tryceratops](https://github.com/guilatrova/tryceratops) | A linter to prevent exceptions being silently ignored. |
| [flake8-print](https://github.com/JBKahn/flake8-print)  | Check for Print statements in python files. |
| [httpx](https://www.python-httpx.org/)                  | A next-generation HTTP client for Python. |
| [starlette](https://www.starlette.io/)                  | Starlette is a lightweight ASGI framework/toolkit, which is ideal for building high-performance asyncio services. |
| [starlette-testclient](https://www.starlette.io/testclient/) | Starlette's test client provides a way to make test requests to an ASGI application. |
| [alembic](https://alembic.sqlalchemy.org/en/latest/)    | Alembic is a lightweight database migration tool for usage with the SQLAlchemy Database Toolkit for Python. |
| [pika-stubs](https://pika.readthedocs.io/en/stable/)    | Type stubs for Pika, an AMQP 0-9-1 client library for Python. |
| [sqlalchemy-utils](https://sqlalchemy-utils.readthedocs.io/en/latest/) | Various utility functions for SQLAlchemy. |
| [types-sqlalchemy-utils](https://pypi.org/project/types-sqlalchemy-utils/) | Typing stubs for SQLAlchemy-Utils. |

</details>



---
