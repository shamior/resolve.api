from typing import Annotated, Sequence

from fastapi import Depends
from sqlmodel import select

from app.database import SessionDep
from app.models.user_model import User


class UserRepositoryFactory:
    def __init__(self, db: SessionDep) -> None:
        self.db = db

    def find_many(self) -> Sequence[User]:
        users = self.db.exec(select(User)).all()
        return users


UserRepository = Annotated[UserRepositoryFactory, Depends()]
