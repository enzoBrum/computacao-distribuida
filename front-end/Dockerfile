FROM python:3.12-alpine3.19 AS base

COPY . app
RUN pip install -r /app/requirements.txt
WORKDIR /app

COPY ../protos/*.py .

CMD ["python", "app.py"]