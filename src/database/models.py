from typing import Optional, Literal

from pydantic import EmailStr
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

from src.database.config import settings

engine = create_async_engine(settings.database_url)
create_async_session = async_sessionmaker(bind=engine, class_=AsyncSession)

async def get_async_session():
    async with create_async_session() as session:
        yield session

Base = declarative_base()


class User(Base):
    __tablename__ = "User"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[Optional[str]] = mapped_column(nullable=False)

    role: Mapped[str] = mapped_column(nullable=False,default="")