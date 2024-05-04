import os
from time import sleep
from typing import Generator, Iterator

from psycopg2 import connect
from psycopg2.extensions import cursor
from contextlib import contextmanager

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_URL = os.getenv("DB_URL")
DB_DATABASE = os.getenv("DB_DATABASE")


@contextmanager
def connect_to_database() -> Iterator[cursor]:
    with connect(database=DB_DATABASE, user=DB_USER, password=DB_PASSWORD, host=DB_URL) as conn, conn.cursor() as cursor:
        yield cursor
