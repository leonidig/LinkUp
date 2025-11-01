from os import getenv
from dotenv import load_dotenv

from aiohttp import ClientSession

load_dotenv()
BACKEND_URL = getenv("BACKEND_URL")


class BackendClient:
    BASE_URL = BACKEND_URL

    @classmethod
    async def _request(cls, method: str, path: str, data: dict | None = None, params: dict | None = None):
        async with ClientSession() as session:
            async with session.request(method, f"{cls.BASE_URL}{path}", json=data, params=params) as resp:
                try:
                    json_data = await resp.json()
                except Exception:
                    json_data = {}
                return resp.status, json_data

    @classmethod
    async def get(cls, path: str, params: dict | None = None) -> tuple[int, dict]:
        return await cls._request("GET", path, params=params)

    @classmethod
    async def post(cls, path: str, data: dict) -> tuple[int, dict]:
        return await cls._request("POST", path, data=data)


    @classmethod
    async def put(cls, path: str, data: dict) -> int:
        status, _ = await cls._request("PUT", path, data=data)
        return status

    @classmethod
    async def delete(cls, path: str, data: dict | None = None) -> int:
        status, _ = await cls._request("DELETE", path, data=data)
        return status