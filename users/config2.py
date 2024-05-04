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


def create_db(cursor: cursor):
    create_user_table = """
    CREATE TABLE IF NOT EXISTS users (
        id_user SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        email VARCHAR(50) NOT NULL UNIQUE,
        password VARCHAR(50) NOT NULL
    );
    CREATE TABLE IF NOT EXISTS polls (
        id_poll SERIAL PRIMARY KEY,
        text VARCHAR(200) NOT NULL,
        title VARCHAR(50) NOT NULL,
        id_creator INT REFERENCES users(id_user) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS option (
        id_option SERIAL PRIMARY KEY,
        text VARCHAR(200) NOT NULL,
        id_poll INT REFERENCES polls(id_poll) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS vote (
        id_voto SERIAL PRIMARY KEY,
        id_user INT REFERENCES users(id_user) ON DELETE CASCADE,
        id_option INT REFERENCES option(id_option) ON DELETE CASCADE
    );
    """
    cursor.execute(create_user_table) 


def init_db():
    """
    Inicializa a base de dados.
    """

    attempts = 1
    while attempts < 30:
        try:
            with connect_to_database() as cursor:
                create_db(cursor)
            return
        except:
            attempts += 1
            sleep(1)
