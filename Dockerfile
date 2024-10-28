FROM python:3.10

# Display output straight to the terminal
ENV PYTHONUNBUFFERED 1

RUN mkdir /app

WORKDIR /app

ADD . /app/

RUN pip install -r requirements.txt
