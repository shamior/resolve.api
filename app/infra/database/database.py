from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, create_engine

from app.domain.config.env_config.settings import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},
)


def get_session():  # pragma: no cover
    with Session(engine) as session:
        yield session


Database = Annotated[Session, Depends(get_session)]
