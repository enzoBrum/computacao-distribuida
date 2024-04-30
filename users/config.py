import os
from time import sleep

from sqlalchemy import Engine, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_URL = os.getenv("DB_URL")
DB_DATABASE = os.getenv("DB_DATABASE")


class Base(MappedAsDataclass, DeclarativeBase): ...


class DbUser(Base):
    """
    Representa a tabela de usuários
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(50))

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, email={self.email!r})"


def engine() -> Engine:
    return create_engine(
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_URL}/{DB_DATABASE}"
    )


def init_db():
    """
    Inicializa a base de dados.
    """

    attempts = 1
    while attempts < 30:
        try:
            Base.metadata.create_all(engine())
            return
        except:
            attempts += 1
            sleep(1)
