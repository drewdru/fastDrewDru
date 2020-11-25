FROM python:3.8

ADD requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

USER root
WORKDIR /app
COPY . /app/
