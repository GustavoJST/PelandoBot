from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message
from tgbot.utils.database import async_db

async def promo(message: Message, bot: AsyncTeleBot):
    if not await async_db.redis.exists(f"{message.chat.id}.state"):
        await bot.send_message(message.chat.id, "Beep boop. Vou começar a puxar novas promoções a partir de agora.")
        await async_db.add_user(message.chat.id)
    
    else:
        await bot.send_message(message.chat.id, "Beep boop. Você já está cadastrado para receber novas promoções. "
                                                "Paciência é uma virtude...")