from telebot.asyncio_filters import SimpleCustomFilter
from telebot.types import Message
from telebot.async_telebot import AsyncTeleBot
from pelandobot.tgbot.utils.database import async_db


class AdminFilter(SimpleCustomFilter):
    """
    Filter for admin users and private chats, since in a private chat,
    the user has the 'member' attribute instead of 'administrator'.
    """

    key = "admin"

    def __init__(self, bot: AsyncTeleBot):
        self._bot = bot

    async def check(self, message: Message):
        if message.chat.type in ["private"]:
            return True
        # Cache all chat admin IDs in the database for 1 hour.
        if not await async_db.redis.exists(f"{message.chat.id}.admins"):
            admin_ids = [
                admin.user.id for admin in await self._bot.get_chat_administrators(message.chat.id)
            ]
            await async_db.redis.sadd(f"{message.chat.id}.admins", *admin_ids)
            await async_db.redis.expire(f"{message.chat.id}.admins", 3600)

        return (
            True
            if await async_db.redis.sismember(f"{message.chat.id}.admins", message.from_user.id)
            else False
        )
