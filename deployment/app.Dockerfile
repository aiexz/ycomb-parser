FROM python:3.10.9-slim-buster

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        # deps for installing poetry
        curl \
        # deps for building python deps
        build-essential \
    && apt-get install -y --no-install-recommends build-essential gcc git && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

RUN mkdir /app

COPY pyproject.toml /app

WORKDIR /app

ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY . /app

CMD poetry run uvicorn --host=0.0.0.0 app.main:app