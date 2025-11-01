import asyncio

from uvicorn import run as run_asgi

from server import app
from server.db import AsyncDB


async def main():
    await AsyncDB.down()
    await AsyncDB.up()


if __name__ == "__main__":
    asyncio.run(main())
    run_asgi(app)