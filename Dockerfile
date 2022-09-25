FROM ubuntu:20.04

RUN apt update

RUN apt-get install python3.9 -y

RUN mkdir /app

COPY . /app

RUN export LANG=ru_RU.UTF-8

WORKDIR /app

RUN chmod +x /app/geckodriver

RUN apt-get install python3-pip -y

RUN python3.9 -m pip install -r /app/requirements.txt

RUN apt-get install firefox -y
