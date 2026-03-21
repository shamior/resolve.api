from collections.abc import Sequence
from typing import Annotated

from fastapi import Depends
from pydantic import UUID4
from sqlmodel import col, or_, select

from app.infra.database.database import Database
from app.infra.database.models import Service


class ServiceRepositoryFactory:
    def __init__(self, db: Database) -> None:
        self.__db = db

    @staticmethod
    def __get_select_clause(retrieve_deleted=False):
        select_clause = select(Service)
        if not retrieve_deleted:
            select_clause = select_clause.where(
                col(Service.deleted_at).is_(None),
            )
        return select_clause

    def find_many(self) -> Sequence[Service]:
        services = self.__db.exec(self.__get_select_clause()).all()
        return services

    def find_related_to_user(self, user_id: UUID4):
        services = self.__db.exec(
            self.__get_select_clause().where(
                or_(
                    Service.comercial_id == user_id,
                    Service.executor == user_id,
                ),
            ),
        ).all()
        return services


ServiceRepository = Annotated[ServiceRepositoryFactory, Depends()]
