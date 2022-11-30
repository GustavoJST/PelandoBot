# aioredis
from redis import asyncio as aioredis

# Create a connection
class Database:
    def __init__(self) -> None:
        self.redis = aioredis.from_url("redis://localhost", decode_responses=True)
    
    async def add_user(self, chat_id):
       await self.redis.rpush("users", chat_id)
        
    async def remove_user(self, chat_id):
       await self.redis.lrem(name="users", count=1, value=chat_id)
    
    async def get_current_users(self):
        return await self.redis.lrange(name="users", start=0, end=-1)

# Instantiate database to be used across the project with import.
db = Database()