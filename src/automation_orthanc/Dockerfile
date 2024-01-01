FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy
LABEL authors="tugrulcansollu"
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

RUN apt-get update && apt-get install -y  \
    libpq-dev python3-dev gcc postgresql \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean


WORKDIR /floy
COPY ./ /

RUN ls -la
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install
