
import aiohttp
from src.utils.external_api.config import API_KEY, API_URL
headers = {'apikey': API_KEY}


async def get_all_currencies():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(API_URL + "/list", headers=headers) as response:
                response.raise_for_status()
                data = await response.json()
                return data
        except Exception as e:
            print(e)

async def get_change_data(start_date: str, end_date: str):
    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            async  with session.get(API_URL + f"/change?start_date={start_date}&end_date={end_date}") as response:
                response.raise_for_status()
                data = await response.json()
                return data
        except Exception as e:
            print(e)





