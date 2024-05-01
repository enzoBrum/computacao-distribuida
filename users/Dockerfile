FROM python:3.12-alpine3.19 AS base

RUN mkdir /app
COPY requirements.txt app/
RUN pip install --no-cache-dir -r /app/requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/protos"
ENV PYTHONDONTWRITEBYTECODE 1

COPY . app/

WORKDIR /app

CMD ["python", "app.py"]
