from fastapi import APIRouter, Depends

from src.auth.dependencies import get_repository
from src.repositories.base_repository import Repository
from src.utils.external_api.connection import get_all_currencies, get_change_data

ext_api = APIRouter()


@ext_api.post("/list")
async def get_currency_list(token: str, repo: Repository = Depends(get_repository)):
    return await repo.verify_role(token, get_all_currencies)

@ext_api.post("/change")
async def get_change_cur(start_date: str, end_date: str):
    return await get_change_data(start_date, end_date)