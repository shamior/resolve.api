from typing import List, Optional

from app.models.client_model import ClientPresentable, DocumentPresentable
from app.models.payment.accordance_model import AccordancePresentable
from app.models.payment.judicial_notification_model import (
    JudicialNotificationPresentable,
)
from app.models.payment.payment_model import PaymentPresentable
from app.models.payment.receipt_model import ReceiptPresentable
from app.models.payment.repass_model import RepassPresentable
from app.models.services.appointment_model import AppointmentPresentable
from app.models.services.service_field_model import ServiceFieldPresentable
from app.models.services.service_field_type_model import (
    ServiceFieldTypePresentable,
)
from app.models.services.service_model import ServicePresentable
from app.models.services.service_notes_model import ServiceNotesPresentable
from app.models.services.service_status_model import ServiceStatusPresentable
from app.models.services.service_type_model import ServiceTypePresentable
from app.models.user_model import UserPresentable


class UserAggregate(UserPresentable):
    services_as_executor: List["ServicePresentable"]
    services_as_comercial: List["ServicePresentable"]
    repasses: List["RepassPresentable"]


class ServiceAggregate(ServicePresentable):
    executor: "UserPresentable"
    comercial: "UserPresentable"
    status: "ServiceStatusPresentable"
    client: "ClientAggregateWithDocuments"
    appointments: List["AppointmentPresentable"]
    payments: List["PaymentAggregate"]
    notes: List["ServiceNotesPresentable"]
    service_type: "ServiceTypePresentable"
    service_fields: List["ServiceFieldAggregate"]


class ServiceFieldAggregate(ServiceFieldPresentable):
    field_type: ServiceFieldTypePresentable


class ClientAggregate(ClientPresentable):
    services: List["ServicePresentable"]
    documents: List["DocumentPresentable"]


class ClientAggregateWithDocuments(ClientPresentable):
    documents: List["DocumentPresentable"]


class PaymentAggregate(PaymentPresentable):
    receipt: Optional["ReceiptPresentable"]
    repasses: List["RepassPresentable"]
    accordance: Optional["AccordancePresentable"]
    notification: Optional["JudicialNotificationPresentable"]
