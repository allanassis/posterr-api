FROM python:3.9.12-buster

ENV HOME=/usr/local/lib
ENV ENV=docker
ENV PYTHONUNBUFFERED=1

EXPOSE 8080

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install --no-install-recommends -y curl \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python \
    && rm -rf /var/lib/apt/lists/*

ENV PATH=$HOME/.poetry/bin:$PATH

RUN poetry install