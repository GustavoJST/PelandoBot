from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message
from pelandobot.tgbot.utils.database import async_db


async def promo(message: Message, bot: AsyncTeleBot):
    if await async_db.redis.scard("active.chats.id") >= 1000 and not await async_db.redis.sismember("active.chats.id", message.chat.id):
        bot.send_message(message.chat.id, "Desculpe. Não posso te enviar promoções pois a lista de membros está cheia.")
        return

    if not await async_db.redis.sismember("active.chats.id", message.chat.id):
        await async_db.add_user(message.chat.id)
        await bot.send_message(message.chat.id, "Vou começar a puxar novas promoções a partir de agora.")

    else:
        await bot.send_message(message.chat.id, "Você já está cadastrado para receber novas promoções. "
                                                "Paciência é uma virtude...")
