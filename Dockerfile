FROM python:3.9-alpine

RUN mkdir /app

COPY . /app

WORKDIR /app

RUN apk add firefox

RUN python -m pip install -r /app/requirements.txt
