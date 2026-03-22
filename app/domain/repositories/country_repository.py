from typing import Annotated

from fastapi import Depends
from sqlmodel import select

from app.infra.database.database import Database
from app.infra.database.models import Country


class CountryRepository:
    def __init__(self, db: Database):
        self.db = db

    def find_many(self):
        query = select(Country)
        return self.db.exec(query).all()

    def find_by_code(self, code: str):
        query = select(Country).where(Country.code == code)
        return self.db.exec(query).first()


CountryRepositoryDep = Annotated[CountryRepository, Depends()]
