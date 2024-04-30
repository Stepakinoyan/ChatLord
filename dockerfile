FROM ubuntu:18.04
FROM python:3.11

RUN mkdir code
WORKDIR /code
COPY pyproject.toml /code


RUN apt-get update && apt-get install -y ffmpeg

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

COPY . .