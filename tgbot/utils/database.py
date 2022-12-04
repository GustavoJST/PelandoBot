# aioredis
from redis import asyncio as aioredis
from redis import Redis

# Create a connection
class AsyncDatabase:
    def __init__(self) -> None:
        self.redis = aioredis.from_url("redis://localhost", decode_responses=True)      
    
    async def add_user(self, chat_id):
        # Se é já existe uma lista com os ids dos usuários ativos, por que guardar o estado do ID em outro lugar?
        # Resposta: talvez seja útil devido a necessidade de impedir o usuário de ser adicionado varias vezes.
        # Exemplo: spammar o comando /start.
        if not await self.redis.exists(f"{chat_id}.state"):
            await self.redis.set(f"{chat_id}.state", "active")
            await self.redis.rpush("active.users.id", chat_id)
        
    async def remove_user(self, chat_id):
        await self.redis.delete(f"{chat_id}.state")
        await self.redis.lrem("active.users.id", 1, chat_id)
        
    async def set_user_tags(self, chat_id, tags):
        if self.redis.exists(f"{chat_id}.tags"):
            await self.redis.delete(f"{chat_id}.tags")
        await self.redis.rpush(f"{chat_id}.tags", tags)
            
    async def unset_user_tags(self, chat_id):
        await self.redis.delete(f"{chat_id}.tags")
        
  
class SyncDatabase:
    def __init__(self) -> None:
        self.redis = Redis.from_url("redis://localhost", decode_responses=True)      


# Instantiates a async database to be used across the project with import.
async_db = AsyncDatabase()

# Instantiates a sync version of the databas to be used in across the project with import.
sync_db = SyncDatabase()