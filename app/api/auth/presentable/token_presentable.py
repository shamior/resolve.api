from pydantic import BaseModel

from app.api.user.presentable.user_presentable import UserPresentable


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenWithUser(Token):
    user: UserPresentable
