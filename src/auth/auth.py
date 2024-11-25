
from fastapi import APIRouter, Depends
from src.auth.dependencies import get_repository
from src.auth.schemas import UserCreate
from src.repositories.base_repository import Repository

reg = APIRouter(prefix="/register")



@reg.post("/")
async def add_user(user: UserCreate, repo: Repository = Depends(get_repository)):
    return await repo.create_user(user)


# @reg.post("/login", response_model=Token)
# async def login(form_data: OAuth2PasswordBearer, session: AsyncSession = Depends(get_async_session)):
#     ...