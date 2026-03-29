from datetime import datetime
from enum import Enum
from typing import Annotated

from fastapi import Depends
from pydantic import UUID4, BaseModel, Field
from sqlmodel import col, func, or_, select

from app.domain.entities.client_entity import LoggedInAs
from app.infra.database.database import Database
from app.infra.database.models import Client


class QueryType(Enum):
    NOT_DELETED = "NOT_DELETED"
    ALL = "ALL"


class ClientRepositoryFindManyFilters(BaseModel):
    offset: int = Field(default=0, ge=0)
    limit: int | None = Field(default=None, ge=1)
    name_phone_or_email: str = Field(default="")
    query_type: QueryType = Field(default=QueryType.NOT_DELETED)
    logged_in_as: LoggedInAs | None = Field(default=None)


class ClientRepository:
    def __init__(self, db: Database):
        self.db = db

    def find_many(
        self,
        filters: ClientRepositoryFindManyFilters,
    ):
        query = select(Client)

        if filters.query_type == QueryType.NOT_DELETED:
            query = query.where(col(Client.deleted_at).is_(None))

        if filters.name_phone_or_email:
            query = query.where(
                or_(
                    col(Client.name).icontains(filters.name_phone_or_email),
                    col(Client.phone).icontains(filters.name_phone_or_email),
                    col(Client.email).icontains(filters.name_phone_or_email),
                ),
            )
        if filters.logged_in_as:
            query = query.where(
                col(Client.logged_in_as) == filters.logged_in_as,
            )

        count_query = select(func.count()).select_from(query.subquery())
        if filters.offset:
            query = query.offset(filters.offset)
        if filters.limit:
            query = query.limit(filters.limit)
        with self.db.begin_nested():
            clients = self.db.exec(query).all()
            count = self.db.exec(count_query).one()
        return clients, count

    def find_by_id(self, client_id: UUID4):
        query = select(Client).where(col(Client.id) == client_id)
        return self.db.exec(query).first()

    def create(self, client: Client):
        self.db.add(client)
        self.db.commit()
        self.db.refresh(client)

    def update(self, client: Client):
        client.updated_at = datetime.now()
        self.db.add(client)
        self.db.commit()
        self.db.refresh(client)
        return client


ClientRepositoryDep = Annotated[ClientRepository, Depends()]
