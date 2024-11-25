from fastapi import APIRouter, Depends

from src.auth.dependencies import get_repository
from src.auth.schemas import Token, UserLogin
from src.repositories.base_repository import Repository

api = APIRouter()

@api.get("/get_all_users")
async def get_users(repo: Repository = Depends(get_repository)):
    return await repo.get_users()

@api.post("/login", response_model=Token)
async def login(user: UserLogin, repo: Repository = Depends(get_repository)):
    return await repo.verify_user(user)

@api.get("/users/me")
async def get_me(token: str, repo: Repository = Depends(get_repository)):
    return await repo.decode_token(token)




