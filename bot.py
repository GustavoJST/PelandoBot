import asyncio
import promotion_query
import logging
from telebot import logger

# Types
from telebot.types import BotCommand, BotCommandScopeAllPrivateChats

# Filters
from tgbot.filters.admin_filter import AdminFilter 

# States
from telebot.asyncio_storage import StateRedisStorage
from telebot.asyncio_filters import StateFilter
from tgbot.states.register_state import UserStates

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
from tgbot.middlewares.group_migration_check import GroupMigrationMiddleware

# Synchronous database
from tgbot.utils.database import sync_db

# Telebot
from telebot.async_telebot import AsyncTeleBot

# Config
from tgbot import config

CHAT_TYPES = ["private", "group", "supergroup"]

bot = AsyncTeleBot(config.TOKEN, state_storage=StateRedisStorage(prefix="state."))
logger.setLevel(logging.DEBUG)

# Cleans database on bot startup.
def clean_db():
    # Cleans all promotions control related tables, as they will be
    # populated later with updated data in promotion_query.py.
    sync_db.redis.delete("unsent.promotions.id")
    if sync_db.redis.exists("promotions.id"):
        promotions_id = sync_db.redis.lrange("promotions.id", 0, -1)
        for id in promotions_id:
            sync_db.redis.delete(f"promotion.{id}.info")
            sync_db.redis.delete(f"promotion.{id}.tags")
    
    # Reset /tags state for active users.
    users_id = sync_db.redis.smembers("active.chats.id")
    for user_id in users_id:
        sync_db.redis.delete(f"state.{user_id}")
    
async def bot_run():
    def register_handlers():
        bot.register_message_handler(start, commands=['start'], chat_types=CHAT_TYPES, admin=True, 
                                     pass_bot=True, content_types=["text"])
        
        bot.register_message_handler(promo, commands=['promo'], chat_types=CHAT_TYPES, admin=True, 
                                     pass_bot=True, content_types=["text"])
        
        bot.register_message_handler(stop, commands=['stop'], chat_types=CHAT_TYPES, 
                                     admin=True, pass_bot=True, content_types=["text"])
        
        bot.register_message_handler(help, commands=['help'], chat_types=CHAT_TYPES, 
                                     admin=True, pass_bot=True, content_types=["text"])
        
        bot.register_message_handler(tags, commands=['tags'], chat_types=CHAT_TYPES, 
                                     admin=True, pass_bot=True, content_types=["text"])
        
        bot.register_callback_query_handler(callback=tag_option_handler, pass_bot=True, chat_types=CHAT_TYPES,
                                            func=lambda call: True, state=UserStates.tags_button)
        
        bot.register_message_handler(handle_tags_input, chat_types=CHAT_TYPES, admin=True, pass_bot=True,
                                    content_types=["text"], state=[UserStates.tags_remove, UserStates.tags_add])
    register_handlers()
    
    # Bot commands menu for private chats only.
    await bot.set_my_commands(commands=[BotCommand("promo", "Inicia o bot"),
                                        BotCommand("stop", "Para o bot"),
                                        BotCommand("help", "Informações sobre os comandos e o bot"),
                                        BotCommand("tags", "Adicionar/remover tags")],
                                        scope=BotCommandScopeAllPrivateChats())

    # Middlewares
    bot.setup_middleware(AntiFloodMiddleware(limit=2, bot=bot))
    bot.setup_middleware(GroupMigrationMiddleware(bot))

    # custom filters
    bot.add_custom_filter(AdminFilter(bot))
    bot.add_custom_filter(StateFilter(bot))
    
    await bot.polling(non_stop=True)

async def main():
    clean_db()
    await asyncio.gather(bot_run(), promotion_query.get_promotions())   
        
if __name__ == "__main__":
    asyncio.run(main())