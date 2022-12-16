from telebot.asyncio_filters import SimpleCustomFilter
from tgbot.models.users_model import Admin
from telebot import types


class AdminFilter(SimpleCustomFilter):
    """
    Filter for admin users and private chats, since in a private chat,
    the user has the 'member' attribute instead of 'administrator'.
    """
    
    key = 'admin'
    
    def __init__(self, bot):
        self._bot = bot

    async def check(self, message):
        if message.chat.type in ["private"]:
            return True
        
        elif isinstance(message, types.CallbackQuery):
            result = await self._bot.get_chat_member(message.message.chat.id, message.from_user.id)
            return result.status ('creator', 'administrator')
        result = await self._bot.get_chat_member(message.chat.id, message.from_user.id)
        return result.status in ['creator', 'administrator']