import asyncio
import promotion_query
import logging
from telebot import logger
from telebot.types import BotCommand, BotCommandScopeAllPrivateChats
# from telebot import custom_filters

# Filters
from tgbot.filters.admin_filter import AdminFilter

# Handlers
from tgbot.handlers.admin import admin_user
from tgbot.handlers.spam_command import anti_spam
from tgbot.handlers.start import start
from tgbot.handlers.tags import tags
from tgbot.handlers.stop import stop
from tgbot.handlers.promo import promo
from tgbot.handlers.help import help

# Callbacks
from tgbot.callbacks.callback_tags import tag_option_handler, handle_tags_input


# Middlewares
from tgbot.middlewares.antiflood_middleware import AntiFloodMiddleware

# Synchronous database
from tgbot.utils.database import sync_db

# Asynchronous database
from tgbot.utils.database import async_db

# Telebot
from telebot.async_telebot import AsyncTeleBot

# Config
from tgbot import config


bot = AsyncTeleBot(config.TOKEN)
logger.setLevel(logging.DEBUG)

def clean_db():
    # Cleans all promotions control related tables, as they will be
    # populated later with updated data in promotion_query.py.
    sync_db.redis.delete("unsent.promotions.id")
    if sync_db.redis.exists("promotions.id"):
        promotions_id = sync_db.redis.lrange("promotions.id", 0, -1)
        for id in promotions_id:
            sync_db.redis.delete(f"promotion.{id}.info")
    
    # Reset /tags button state for active users.
    users_id = sync_db.redis.smembers("active.users.id")
    for user_id in users_id:
        sync_db.redis.delete(f"{user_id}.tags.button.state")
    
async def bot_run():
    def register_handlers():
        bot.register_message_handler(start, commands=['start'], pass_bot=True)
        bot.register_message_handler(promo, commands=['promo'], pass_bot=True)
        bot.register_message_handler(stop, commands=['stop'], pass_bot=True)
        bot.register_message_handler(help, commands=['help'], pass_bot=True)
        bot.register_message_handler(tags, commands=['tags'], pass_bot=True)
        bot.register_callback_query_handler(callback=tag_option_handler, func=lambda call: True, pass_bot=True)
        bot.register_message_handler(handle_tags_input, content_types=["text"], 
                                     func=lambda message: sync_db.redis.exists(f"{message.chat.id}.state.tags.reply") == 1, 
                                     pass_bot=True)
        
    register_handlers()
    
    # TODO: colocar todos os comandos futuramente.
    await bot.set_my_commands(commands=[BotCommand("promo", "Inicia o bot"),
                                        BotCommand("stop", "Para o bot"),
                                        BotCommand("help", "Informações sobre comandos e o bot"),
                                        BotCommand("tags", "Adicionar/remover tags")],
                                        scope=BotCommandScopeAllPrivateChats())

    # Middlewares
    bot.setup_middleware(AntiFloodMiddleware(limit=2, bot=bot))

    # custom filters
    # TODO: Remove AdminFilter later.
    bot.add_custom_filter(AdminFilter())
    
    await bot.polling(non_stop=True)

async def main():
    clean_db()
    await asyncio.gather(bot_run(), promotion_query.get_promotions())   
        
if __name__ == "__main__":
    asyncio.run(main())