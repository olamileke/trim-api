FROM python:3.6.15-slim-buster

RUN mkdir -p /app

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y python3 python3-pip python-dev build-essential gcc

RUN pip3 install psycopg2-binary

RUN pip3 install -r requirements.txt --no-cache-dir

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]


