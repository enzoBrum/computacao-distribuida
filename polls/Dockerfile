FROM python:3.12-alpine3.19 AS base

RUN mkdir /app
COPY requirements.txt app/
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY --from=protos *.py app/

COPY . app/

WORKDIR /app

CMD ["python", "app.py"]
