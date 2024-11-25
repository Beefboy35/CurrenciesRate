from typing import Literal

from pydantic import BaseModel


class UserResponse(BaseModel):
    name: str
    email: str
    role: str


class UserLogin(BaseModel):
    name: str
    password: str
class UserCreate(UserResponse):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    name: str | None
    email: str
    expiration: str
    role: str
