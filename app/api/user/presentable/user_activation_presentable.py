from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, EmailStr

from app.domain.entities.user_entity import UserRoles


class UserActivationPresentable(BaseModel):
    id: UUID4
    name: str
    email: EmailStr
    role: UserRoles
    activated_at: Optional[datetime]
