# aioredis
from redis import asyncio as aioredis
from redis import Redis

# Create a connection
class AsyncDatabase:
    def __init__(self) -> None:
        self.redis = aioredis.from_url("redis://localhost", decode_responses=True)      
    
    async def add_user(self, chat_id: int) -> None:
        await self.redis.set(f"{chat_id}.state", "active", nx=True)
        await self.redis.sadd("active.users.id", chat_id)
        if await self.redis.exists(f"{chat_id}.tags"):
            await self.redis.persist(f"{chat_id}.tags")
        
    async def remove_user(self, chat_id: int) -> None:
        await self.redis.delete(f"{chat_id}.state")
        await self.redis.srem("active.users.id", chat_id)
        await self.redis.delete(f"{chat_id}.tags.button.state")
        if await self.redis.exists(f"{chat_id}.tags"):
            await self.redis.expire(f"{chat_id}.tags", 5184000)  # 2 months in seconds.
        
    async def set_user_tags(self, chat_id: int, tags: list) -> None:
        await self.redis.sadd(f"{chat_id}.tags", *tags)
            
    async def unset_user_tags(self, chat_id: int) -> None:
        await self.redis.delete(f"{chat_id}.tags")
        
  
class SyncDatabase:
    def __init__(self) -> None:
        self.redis = Redis.from_url("redis://localhost", decode_responses=True)      


# Instantiates a async database to be used across the project with import.
async_db = AsyncDatabase()

# Instantiates a sync version of the databas to be used in across the project with import.
sync_db = SyncDatabase()