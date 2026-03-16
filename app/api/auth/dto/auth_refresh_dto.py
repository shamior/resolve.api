from pydantic import BaseModel


class RefreshDTO(BaseModel):
    refresh_token: str
