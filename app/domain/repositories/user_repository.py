from typing import Annotated, Sequence

from fastapi import Depends
from sqlmodel import select

from app.infra.database.database import Database
from app.infra.database.models import User


class UserRepositoryFactory:
    def __init__(self, db: Database) -> None:
        self.db = db

    def find_many(self) -> Sequence[User]:
        users = self.db.exec(select(User)).all()
        return users


UserRepository = Annotated[UserRepositoryFactory, Depends()]
