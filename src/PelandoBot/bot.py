import asyncio
import pelandobot.promotion_scraper as promotion_scraper
import logging
import ssl
from aiohttp import web
from telebot import logger
from multiprocessing import Process

# Types.
from telebot.types import BotCommand, BotCommandScopeAllPrivateChats, Update

# Filters.
from pelandobot.tgbot.filters.admin_filter import AdminFilter

# States.
from telebot.asyncio_storage import StateRedisStorage
from telebot.asyncio_filters import StateFilter
from pelandobot.tgbot.states.register_state import UserStates

# Handlers.
from pelandobot.tgbot.handlers.start import start
from pelandobot.tgbot.handlers.tags import tags
from pelandobot.tgbot.handlers.stop import stop
from pelandobot.tgbot.handlers.promo import promo
from pelandobot.tgbot.handlers.help import help

# Callbacks.
from pelandobot.tgbot.callbacks.callback_tags import tag_option_handler, handle_tags_input

# Middlewares.
from pelandobot.tgbot.middlewares.antiflood_middleware import AntiFloodMiddleware
from pelandobot.tgbot.middlewares.group_migration_check import GroupMigrationMiddleware

# Synchronous database.
from pelandobot.tgbot.utils.database import sync_db

# Telebot.
from telebot.async_telebot import AsyncTeleBot

# Config.
from pelandobot.tgbot.config import TOKEN, HOST

WEBHOOK_HOST = HOST
WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port need to be 'open').
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP address.

# Quick'n'dirty SSL certificate generation:
#
# openssl genrsa -out webhook_pkey.pem 2048
# openssl req -new -x509 -days 3650 -key webhook_pkey.pem -out webhook_cert.pem
#
# When asked for "Common Name (e.g. server FQDN or YOUR name)" you should reply
# with the same value in you put in WEBHOOK_HOST.
WEBHOOK_SSL_CERT = './webhook_cert_dev.pem'  # Path to the ssl certificate.
WEBHOOK_SSL_PRIV = './webhook_pkey_dev.pem'  # Path to the ssl private key.
WEBHOOK_URL_BASE = "https://{}:{}".format(WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(TOKEN)

CHAT_TYPES = ["private", "group", "supergroup"]

bot = AsyncTeleBot(TOKEN, state_storage=StateRedisStorage(prefix="state."))
logger = logger
logger.setLevel(logging.DEBUG)


# Cleans database on bot startup.
def clean_db() -> None:
    # Cleans all promotions control related tables, as they will be
    # populated later with updated data in promotion_scraper.py.
    if sync_db.redis.exists("unsent.promotions.id"):
        promotions_id = sync_db.redis.lrange("unsent.promotions.id", 0, -1)
        for id in promotions_id:
            sync_db.redis.delete(f"promotion.{id}.info")
            sync_db.redis.delete(f"promotion.{id}.tags")
    sync_db.redis.delete("promotions.id")
    sync_db.redis.delete("unsent.promotions.id")
    
    # Reset /tags state for active users.
    users_id = sync_db.redis.smembers("active.chats.id")
    for user_id in users_id:
        sync_db.redis.delete(f"state.{user_id}")
        

# Process webhook calls.
async def handle(request) -> web.Response:
    if request.match_info.get('token') == bot.token:
        request_body_dict = await request.json()
        update = Update.de_json(request_body_dict)
        asyncio.ensure_future(bot.process_new_updates([update]))
        return web.Response()
    else:
        return web.Response(status=403)


# Remove webhook and closing session before exiting.
async def shutdown(app) -> None:
    logger.info('Shutting down: removing webhook')
    await bot.remove_webhook()
    logger.info('Shutting down: closing session')
    await bot.close_session()


async def bot_setup() -> None:
    # Message handlers and callbacks.
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
        
        bot.register_callback_query_handler(callback=tag_option_handler, pass_bot=True,
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

    # Middlewares.
    bot.setup_middleware(AntiFloodMiddleware(limit=2, bot=bot))
    bot.setup_middleware(GroupMigrationMiddleware(bot))

    # Custom filters.
    bot.add_custom_filter(AdminFilter(bot))
    bot.add_custom_filter(StateFilter(bot))
    

async def setup() -> web.Application:
    # Setup bot.
    await bot_setup()
    # Remove webhook, it fails sometimes the set if there is a previous webhook.
    logger.info('Starting up: removing old webhook')
    await bot.remove_webhook()
    
    # Set webhook.
    logger.info('Starting up: setting webhook')
    await bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))
    app = web.Application()
    app.router.add_post('/{token}/', handle)
    app.on_cleanup.append(shutdown)
    return app


if __name__ == '__main__':
    #clean_db()
    promotion_scraper_process = Process(target=promotion_scraper.PromotionScraper().promotion_scraper_loop).start()
    # Build ssl context.
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)
    # Start aiohttp server.
    web.run_app(
        setup(),
        host=WEBHOOK_LISTEN,
        port=WEBHOOK_PORT,
        ssl_context=context,
    )
    