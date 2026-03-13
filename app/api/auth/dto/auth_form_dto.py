from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
