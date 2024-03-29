from telebot.asyncio_handler_backends import BaseMiddleware
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message
from pelandobot.tgbot.utils.database import async_db


class GroupMigrationMiddleware(BaseMiddleware):
    def __init__(self, bot: AsyncTeleBot) -> None:
        # Always specify update types, otherwise middlewares won't work.
        self.update_types = ["message"]
        self.bot = bot

    async def pre_process(self, message: Message, data):
        if message.migrate_to_chat_id is not None:
            old_id = message.chat.id
            new_id = message.migrate_to_chat_id
            if await async_db.redis.sismember("active.chats.id", old_id):
                await async_db.redis.srem("active.chats.id", old_id)
                await async_db.redis.sadd("active.chats.id", new_id)

                for state in ["tags.", "state."]:
                    if await async_db.redis.exists(f"{state}{old_id}"):
                        await async_db.redis.rename(f"{state}{old_id}", f"{state}{new_id}")

    # Don't delete this or it'll raise NotImplementedError.
    async def post_process(self, message, data, exception):
        pass
