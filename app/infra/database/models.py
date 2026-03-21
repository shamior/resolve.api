import uuid
from typing import List, Optional

from pydantic import UUID4
from sqlmodel import Field, Relationship, SQLModel

from app.domain.entities.accordance_entity import AccordanceEntity
from app.domain.entities.appointment_entity import AppointmentEntity
from app.domain.entities.client_entity import ClientEntity
from app.domain.entities.document_entity import DocumentEntity
from app.domain.entities.judicial_notification_entity import (
    JudicialNotificationEntity,
)
from app.domain.entities.payment_entity import PaymentEntity
from app.domain.entities.receipt_entity import ReceiptEntity
from app.domain.entities.repass_entity import RepassEntity
from app.domain.entities.service_entity import ServiceEntity
from app.domain.entities.service_field_entity import ServiceFieldEntity
from app.domain.entities.service_field_type_entity import (
    ServiceFieldTypeEntity,
)
from app.domain.entities.service_notes_entity import ServiceNotesEntity
from app.domain.entities.service_status_entity import ServiceStatusEntity
from app.domain.entities.service_type_entity import ServiceTypeEntity
from app.domain.entities.user_entity import UserEntity
from app.domain.entities.user_role_entity import RoleType, UserRoleEntity
from app.domain.entities.with_date_entity import WithDateModel


class RoleLink(SQLModel, table=True):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)

    user_id: UUID4 = Field(..., foreign_key="user.id", primary_key=True)
    role_id: UUID4 = Field(..., foreign_key="userrole.id", primary_key=True)


class User(UserEntity, WithDateModel, table=True):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)
    roles: List["UserRole"] = Relationship(
        back_populates="users",
        link_model=RoleLink,
    )

    services_as_executor: List["Service"] = Relationship(
        back_populates="executor",
        sa_relationship_kwargs={"foreign_keys": "Service.executor_id"},
    )
    services_as_comercial: List["Service"] = Relationship(
        back_populates="comercial",
        sa_relationship_kwargs={"foreign_keys": "Service.comercial_id"},
    )

    repasses: List["Repass"] = Relationship(back_populates="receiver")
    service_notes: List["ServiceNotes"] = Relationship(back_populates="issuer")


class UserRole(UserRoleEntity, table=True):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)

    role_type: "RoleType" = Field(
        ...,
        description="Tipo de cargo do usuário",
        unique=True,
    )
    users: List["User"] = Relationship(
        back_populates="roles",
        link_model=RoleLink,
    )


class Document(DocumentEntity, WithDateModel, table=True):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)

    client: "Client" = Relationship(back_populates="documents")


class Client(ClientEntity, WithDateModel, table=True):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)

    services: List["Service"] = Relationship(back_populates="client")
    documents: List["Document"] = Relationship(back_populates="client")


class FieldLink(SQLModel, table=True):
    service_type_id: UUID4 = Field(
        foreign_key="servicetype.id",
        primary_key=True,
    )
    field_type_id: UUID4 = Field(
        foreign_key="servicefieldtype.id",
        primary_key=True,
    )


class ServiceType(ServiceTypeEntity, WithDateModel, table=True):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)
    services: List["Service"] = Relationship(back_populates="service_type")
    field_types: List["ServiceFieldType"] = Relationship(
        back_populates="service_types",
        link_model=FieldLink,
    )


class ServiceStatus(ServiceStatusEntity, WithDateModel, table=True):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)


class ServiceNotes(ServiceNotesEntity, WithDateModel, table=True):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)
    service: "Service" = Relationship(back_populates="service_notes")
    issuer: "User" = Relationship(back_populates="service_notes")


class Service(ServiceEntity, WithDateModel, table=True):
    id: int | None = Field(primary_key=True)

    executor: "User" = Relationship(
        back_populates="services_as_executor",
        sa_relationship_kwargs={"foreign_keys": "Service.executor_id"},
    )
    comercial: "User" = Relationship(
        back_populates="services_as_executor",
        sa_relationship_kwargs={"foreign_keys": "Service.comercial_id"},
    )

    status: "ServiceStatus" = Relationship()
    client: "Client" = Relationship(back_populates="services")
    service_type: "ServiceType" = Relationship(back_populates="services")

    appointments: List["Appointment"] = Relationship(back_populates="service")
    payments: List["Payment"] = Relationship(back_populates="service")
    service_notes: List["ServiceNotes"] = Relationship(
        back_populates="service",
    )
    service_fields: List["ServiceField"] = Relationship(
        back_populates="service",
    )


class ServiceFieldType(ServiceFieldTypeEntity, WithDateModel, table=True):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)
    service_fields: List["ServiceField"] = Relationship(
        back_populates="field_type",
    )
    service_types: List["ServiceType"] = Relationship(
        back_populates="field_types",
        link_model=FieldLink,
    )


class ServiceField(ServiceFieldEntity, WithDateModel, table=True):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)
    service: "Service" = Relationship(back_populates="service_fields")
    field_type: "ServiceFieldType" = Relationship(
        back_populates="service_fields",
    )


class Appointment(AppointmentEntity, WithDateModel, table=True):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)
    service: "Service" = Relationship(back_populates="appointments")


class Repass(RepassEntity, WithDateModel, table=True):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)

    receipt: Optional["Receipt"] = Relationship(back_populates="repass")
    payment: "Payment" = Relationship(back_populates="repasses")
    receiver: "User" = Relationship(back_populates="repasses")


class Receipt(ReceiptEntity, WithDateModel, table=True):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)

    payment: Optional["Payment"] = Relationship(back_populates="receipt")
    repass: Optional["Repass"] = Relationship(back_populates="receipt")


class Payment(PaymentEntity, WithDateModel, table=True):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)

    service: "Service" = Relationship(back_populates="payments")
    repasses: List["Repass"] = Relationship(back_populates="payment")
    receipt: Optional["Receipt"] = Relationship(back_populates="payment")
    accordance: Optional["Accordance"] = Relationship(back_populates="payment")
    notification: Optional["JudicialNotification"] = Relationship(
        back_populates="payment",
    )


class JudicialNotification(
    JudicialNotificationEntity,
    WithDateModel,
    table=True,
):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)

    payment: "Payment" = Relationship(back_populates="notification")


class Accordance(AccordanceEntity, WithDateModel, table=True):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)

    payment: "Payment" = Relationship(back_populates="accordance")
