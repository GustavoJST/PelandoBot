import asyncio
import promotion_query

# filters
from tgbot.filters.admin_filter import AdminFilter

# handlers
from tgbot.handlers.admin import admin_user
from tgbot.handlers.spam_command import anti_spam
from tgbot.handlers.user import any_user

# middlewares
from tgbot.middlewares.antiflood_middleware import AntiFloodMiddleware

# synchronous database
from tgbot.utils.database import sync_db

# telebot
from telebot.async_telebot import AsyncTeleBot

# config
from tgbot import config

bot = AsyncTeleBot(config.TOKEN)

def clean_db():
    sync_db.redis.delete("unsent.promotions.id")
    if sync_db.redis.exists("promotions.id"):
        ids = sync_db.redis.lrange("promotions.id", 0, -1)
        for id in ids:
            sync_db.redis.delete(f"promotion.{id}.info")
    
async def bot_run():
    def register_handlers():
        # bot.register_message_handler(admin_user, commands=['start'], admin=True, pass_bot=True)
        bot.register_message_handler(any_user, commands=['start'], admin=False, pass_bot=True)
        bot.register_message_handler(anti_spam, commands=['spam'], pass_bot=True)

    register_handlers()

    # Middlewares
    bot.setup_middleware(AntiFloodMiddleware(limit=2, bot=bot))

    # custom filters
    bot.add_custom_filter(AdminFilter())

    await bot.polling(non_stop=True)

async def main():
    clean_db()
    await asyncio.gather(bot_run(), promotion_query.get_promotions())   
        
if __name__ == "__main__":
    asyncio.run(main())