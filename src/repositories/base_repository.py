import datetime
from abc import ABC, abstractmethod
from typing import Callable

import jwt
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.auth.config import get_pw_hashed, verify_password, EXPIRATION_SECONDS_LEFT, SECRET_KEY, ALGORITHM
from src.auth.schemas import UserResponse, UserCreate, Token, UserLogin, TokenData
from src.database.models import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="MyToken")


def create_jwt_token(data: dict, expiration: datetime.timedelta):
    data_copy = data.copy()
    expire = datetime.datetime.now(tz=datetime.UTC) + (
        expiration if expiration else datetime.timedelta(seconds=200)
    )
    data_copy.update({"expiration": jsonable_encoder(expire)})
    return jwt.encode(payload=data_copy, key=SECRET_KEY, algorithm=ALGORITHM)


class JWTError(HTTPException):
    def __init__(self, status, detail):
        super().__init__(status_code=status, detail=detail)


class Repository(ABC):  # это абстрактный интерфейс нашего репозитория
    @abstractmethod
    async def get_users(self) -> list[UserResponse]:
        pass

    @abstractmethod
    async def create_user(self, user: UserCreate) -> UserResponse:
        pass

    @abstractmethod
    async def verify_user(self, user: UserLogin):
        pass

    @abstractmethod
    async def decode_token(self, token: str):
        pass

    @abstractmethod
    async def verify_role(self, token: str, api_func: Callable):
        pass


class SqlAlchemyRepository(
    Repository):  # это его конкретное исполнение для алхимии (можно сделать для peewee, pony и тд, легко поменять способ реализации)
    def __init__(self, session: AsyncSession):  # при инициализации принимает асинхронную сессию
        self.session = session

    # далее, по сути, код из эндпоинтов с предыдущего шага
    async def get_users(self):
        result = await self.session.execute(select(User))
        return result.scalars().all()

    async def create_user(self, user: UserCreate) -> UserResponse:
        new = User(
            name=user.name,
            email=user.email,
            role=user.role,
            hashed_password=get_pw_hashed(user.password)
        )
        query = await self.session.execute(select(User).filter(User.email == user.email))
        query = query.scalar_one_or_none()
        if query:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail={"message": f"User {user.name} already exists"})
        self.session.add(new)
        await self.session.commit()
        await self.session.refresh(new)
        return new

    async def verify_user(self, user: UserLogin):
        query = await self.session.execute(select(User).filter(User.name == user.name))
        result = query.scalars().first()
        if not result or not verify_password(user.password, result.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={'Error': 'Incorrect name or password('},
                headers={"WWW-Authenticate": "Bearer"}
            )
        access_token_time = datetime.timedelta(seconds=EXPIRATION_SECONDS_LEFT)
        token = create_jwt_token({"name": result.name, "email": result.email, "role": result.role}, access_token_time)
        return Token(access_token=token, token_type="Bearer")

    async def decode_token(self, token: str) -> TokenData:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Unknown credentials"},
            headers={"WWW-Authenticate": "Bearer"}
        )
        try:
            payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
            name: str = payload.get("name")
            email: str = payload.get("email")
            expiration: str = payload.get("expiration")
            role: str = payload.get("role")
            if (name, email, expiration, role) is None:
                raise credentials_exception
            return TokenData(name=name, email=email, expiration=expiration, role=role)
        except Exception as e:
            raise JWTError(status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                           detail=f"Something went wrong(, details: {e}")

    async def verify_role(self, token: str, api_func: Callable): # method to check if a user is an admin
        try:
            payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
            role: str = payload.get("role")
        except:
            raise JWTError(status=status.HTTP_400_BAD_REQUEST, detail="Invalid JWT")
        if role != "admin":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"state": "access restricted"}
            )
        else:
            data = await api_func() #call various functions depend on what we want to fetch from external api. CAUTION: api_func must have no arguments
            return data
