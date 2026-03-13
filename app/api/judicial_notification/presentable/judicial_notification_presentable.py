from pydantic import UUID4
from sqlmodel import Field

from app.domain.entities.judicial_notification_entity import (
    JudicialNotificationEntity,
)


class JudicialNotificationPresentable(JudicialNotificationEntity):
    id: UUID4 = Field()
