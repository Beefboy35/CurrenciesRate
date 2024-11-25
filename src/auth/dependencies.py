import datetime
from fastapi import Depends, HTTPException
import jwt

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import get_async_session, User
from src.repositories.base_repository import SqlAlchemyRepository


async def get_repository(session: AsyncSession = Depends(get_async_session)):
    return SqlAlchemyRepository(session)

async def get_users(session: AsyncSession =Depends(get_async_session)):
    test = await session.execute(select(User).where(User.role == "admin"))






