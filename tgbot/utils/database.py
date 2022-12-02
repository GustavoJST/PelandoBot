# aioredis
from redis import asyncio as aioredis
from redis import Redis

# Create a connection
class AsyncDatabase:
    def __init__(self) -> None:
        self.redis = aioredis.from_url("redis://localhost", decode_responses=True)      
    
    async def set_user_state(self, chat_id):
        # Se é já existe uma lista com os ids dos usuários ativos, por que guardar o estado do ID em outro lugar?
        await self.redis.set(f"{chat_id}.state", "active")
        await self.redis.rpush("active.users", chat_id)
        
    async def unset_user_state(self, chat_id):
        await self.redis.set(f"{chat_id}.state", "inactive")
        await self.redis.lrem("active.users", 1, chat_id)
        
    async def remove_user(self, chat_id):
       await self.redis.lrem(name="users", count=1, value=chat_id)
       
    async def set_user_tags(self, chat_id, tags):
        if self.redis.exists(f"{chat_id}.tags"):
            await self.redis.delete(f"{chat_id}.tags")
        await self.redis.rpush(f"{chat_id}.tags", tags)
            
    async def unset_user_tags(self, chat_id):
        await self.redis.delete(f"{chat_id}.tags")
        
    async def get_active_users(self):
        return await self.redis.lrange("active.users", 0, -1)
    
class SyncDatabase:
    def __init__(self) -> None:
        self.redis = Redis.from_url("redis://localhost", decode_responses=True)      

# Instantiate async database to be used across the project with import.
async_db = AsyncDatabase()

# Instantiate a sync version of the databas to be used in the promotion_query process.
sync_db = SyncDatabase()