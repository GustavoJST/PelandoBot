# aioredis
from redis import asyncio as aioredis
from redis import Redis

# Create a connection
class AsyncDatabase:
    def __init__(self) -> None:
        self.redis = aioredis.from_url("redis://localhost", decode_responses=True)      
  
    async def add_user(self, chat_id: int) -> None:
        await self.redis.sadd("active.chats.id", chat_id)
        if await self.redis.exists(f"tags.{chat_id}"):
            await self.redis.persist(f"tags.{chat_id}")
        
    async def remove_user(self, chat_id: int) -> None:
        await self.redis.srem("active.chats.id", chat_id)
        await self.redis.delete(f"state.{chat_id}")
        if await self.redis.exists(f"tags.{chat_id}"):
            await self.redis.expire(f"tags.{chat_id}", 5184000)  # 2 months in seconds.      
  
class SyncDatabase:
    def __init__(self) -> None:
        self.redis = Redis.from_url("redis://localhost", decode_responses=True)    
        
    def add_user(self, chat_id: int) -> None:
        self.redis.sadd("active.chats.id", chat_id)
        if self.redis.exists(f"tags.{chat_id}"):
            self.redis.persist(f"tags.{chat_id}")
            
    def remove_user(self, chat_id: int) -> None:
        self.redis.srem("active.chats.id", chat_id)
        self.redis.delete(f"state.{chat_id}")
        if self.redis.exists(f"tags.{chat_id}"):
            self.redis.expire(f"tags.{chat_id}", 5184000)


# Instantiates a async database to be used across the project with import.
async_db = AsyncDatabase()

# Instantiates a sync version of the database to be used in across the project with import.
sync_db = SyncDatabase()