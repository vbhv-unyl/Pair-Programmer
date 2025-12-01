# app/core/redis_client.py
from redis import asyncio as aioredis
from app.core.config import REDIS_URL

class RedisClient:
    def __init__(self):
        self.client = None

    async def connect(self):
        if not self.client:
            self.client = await aioredis.from_url(
                REDIS_URL,
                decode_responses=True
            )

    async def get(self, key: str):
        await self.connect()
        return await self.client.get(key)

    async def set(self, key: str, value: str):
        await self.connect()
        await self.client.set(key, value)

    async def delete(self, key: str):
        await self.connect()
        await self.client.delete(key)


redis_client = RedisClient()
