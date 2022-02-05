from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from directory.lib.settings import SETTINGS

SQLALCHEMY_DATABASE_URL = SETTINGS.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


@contextmanager
def get_session() -> Session:
    with SessionLocal() as session:
        yield session


def db_dependency() -> Session:
    with get_session() as session:
        yield session
