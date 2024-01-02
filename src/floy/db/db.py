from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.settings import config

engine = create_engine(
    url=(
        f"postgresql://{config.DB_USER}:{config.DB_PASSWORD}@"
        f"{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
    ),
)


def get_db() -> Generator[Session, None, None]:
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
