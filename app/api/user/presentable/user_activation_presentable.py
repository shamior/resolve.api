from datetime import datetime

from pydantic import UUID4, BaseModel, EmailStr


class UserActivationPresentable(BaseModel):
    id: UUID4
    name: str
    email: EmailStr
    activated_at: datetime | None
