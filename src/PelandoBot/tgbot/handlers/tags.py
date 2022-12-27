from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message
from pelandobot.tgbot.utils.database import async_db
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from pelandobot.tgbot.states.register_state import UserStates


async def tags(message: Message, bot: AsyncTeleBot):
    if not await async_db.redis.sismember("active.chats.id", message.chat.id) and await async_db.redis.scard("active.chats.id") >= 1000:
        await bot.send_message(message.chat.id, "Você não pode configurar suas tags pois a lista de usuários ativos está cheia.")
        return

    if not await async_db.redis.sismember("active.chats.id", message.chat.id) and await async_db.redis.scard("active.chats.id") < 1000:
        await bot.send_message(message.chat.id, "Me ative com o comando /promo primeiro antes de configurar suas tags.")
        return

    if await async_db.redis.sismember("active.chats.id", message.chat.id):
        if await async_db.redis.exists(f"state.{message.chat.id}"):
            if message.chat.type in ["group", "supergroup"]:
                await bot.send_message(message.chat.id, "Outra pessoa iniciou a configuração das tags. "
                                                        "Aguarde o seu término ou espere três minutos para usar com esse comando")
            else:
                await bot.send_message(message.chat.id, "Continue com a configuração de tags ou "
                                                        "aguarde três minutos para usar este comando.")
            return

        elif not await async_db.redis.exists(f"tags.{message.chat.id}"):
            await bot.send_message(message.chat.id, "Você atualmente não tem nenhuma tag escolhida.")

        else:
            tags = await async_db.redis.smembers(f"tags.{message.chat.id}")
            await bot.send_message(message.chat.id, f"Você possui {len(tags)} tags. "
                                                    "Lembre-se que o limite máximo do número de tags é 30.\n\n"
                                                    "Suas tags atualmente são: \n\n"
                                                    f"{', '.join({tag for tag in tags})}\n\n")

    add_tags = InlineKeyboardButton("Adicionar tags", callback_data="add_tags")
    remove_tags = InlineKeyboardButton("Remover tags", callback_data="remove_tags")
    clean_tags = InlineKeyboardButton("Limpar todas as tags", callback_data="clean_tags")
    exit_tags = InlineKeyboardButton("Sair", callback_data="exit")
    inline_keyboard = InlineKeyboardMarkup().add(add_tags, remove_tags).add(clean_tags, exit_tags)

    await bot.set_state(message.from_user.id, UserStates.tags_button, message.chat.id)
    await async_db.redis.expire(f"state.{message.chat.id}", 180)
    await bot.send_message(message.chat.id, "O que você deseja fazer?", reply_markup=inline_keyboard)
