FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy
LABEL authors="tugrulcansollu"

RUN apt-get update && apt-get install -y  \
    libpq-dev python3-dev gcc postgresql \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean


WORKDIR /floy
COPY ./src src
COPY ./sample_data sample_data

COPY poetry.lock pyproject.toml ./
RUN ls -la
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

CMD ["python", "./src/automation_orthanc/fill_pacs.py"]
