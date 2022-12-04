from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message
from tgbot.utils.database import async_db

async def stop(message: Message, bot: AsyncTeleBot):
    await bot.send_message(message.chat.id, "Beep boop. Não irei entregar novas promoções de agora em diante.")
    await async_db.remove_user(message.chat.id)