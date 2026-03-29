from datetime import date
from typing import Optional

from factory.base import Factory
from factory.declarations import LazyFunction, Sequence
from faker import Faker
from sqlmodel import Session, select

from app.domain.entities.client_entity import LoggedInAs
from app.domain.repositories.client_repository import ClientRepository
from app.domain.repositories.documents_repository import DocumentsRepository
from app.domain.usecases.document.create_document_usecase import (
    CreateDocumentUseCase,
)
from app.infra.database.models import Client, Country, Document
from app.infra.services.file_storage.local_file_storage import LocalFileStorage

fake = Faker()


class ClientFactory:
    def __new__(
        cls,
        db: Session,
        name: Optional[str] = None,
        phone: Optional[str] = None,
        country_code: Optional[str] = None,
        country_name: Optional[str] = None,
        fetch_country: Optional[bool] = False,
        birthdate: Optional[date] = None,
        email: Optional[str] = None,
        passport: Optional[str] = None,
        logged_in_as: Optional[LoggedInAs] = None,
        documents: Optional[list[str]] = None,
        create_file: bool = False,
        batch_size: int = 1,
    ):

        document_repository = DocumentsRepository(db)
        client_repository = ClientRepository(db)
        file_storage = LocalFileStorage()
        create_document_usecase = CreateDocumentUseCase(
            client_repository=client_repository,
            documents_repository=document_repository,
            file_storage=file_storage,
        )
        if country_name is None:
            country_name = fake.country()
        if country_code is None:
            country_code = fake.country_code(representation="alpha-3")

        if not fetch_country:
            country = Country(code=country_code, name=country_name)
            db.add(country)
        else:
            country = db.exec(
                select(Country).where(Country.code == country_code),
            ).first()

        arguments = {
            "name": name,
            "phone": phone,
            "passport": passport,
            "logged_in_as": logged_in_as,
            "email": email,
            "birthdate": birthdate,
            "country": country,
        }
        not_none_kwargs = {
            key: value for key, value in arguments.items() if value is not None
        }
        clients_from_factory: list[Client] = (
            cls.ClientRealFactory.create_batch(
                batch_size,
                **not_none_kwargs,
            )
        )
        db.add_all(clients_from_factory)
        db.commit()
        for client_validated in clients_from_factory:
            if documents is None:
                documents = [
                    fake.file_name(extension=".pdf") for _ in range(3)
                ]
            for doc in documents:
                if create_file:
                    create_document_usecase.execute(
                        client_id=client_validated.id,
                        name=doc,
                        mime_type="application/pdf",
                        file_content=fake.binary(),
                    )
                else:
                    document = Document(
                        client=client_validated,
                        name=doc,
                        path=fake.file_path(),
                    )
                    db.add(document)
            db.refresh(client_validated)
        return clients_from_factory

    class ClientRealFactory(Factory):
        class Meta:  # type: ignore
            model = Client

        name = LazyFunction(fake.name)
        phone = LazyFunction(fake.phone_number)
        passport = LazyFunction(fake.passport_number)
        logged_in_as = LazyFunction(lambda: fake.enum(LoggedInAs))
        email = Sequence(lambda n: f"email_client{n}@email.com")
        birthdate = LazyFunction(fake.date_of_birth)
