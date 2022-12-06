import bot
import asyncio
import timeit
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from tgbot.utils.database import sync_db

def prepare_process():
    asyncio.run(send_message())

async def send_message():
    start = timeit.default_timer()
    
    while sync_db.redis.exists("unsent.promotions.id"):
        tasks = []
        # TODO: Remove this later
        start = timeit.default_timer()
        active_users_id = sync_db.redis.lrange("active.users.id", 0, -1)
        unsent_promotions = sync_db.redis.lrange("unsent.promotions.id", 0, -1)
       
        for promotion_id in unsent_promotions:
            promotion_info = sync_db.redis.hgetall(f"promotion.{promotion_id}.info")
            image = promotion_info["image"]
            message = (f"🚨  PROMOÇÃO  🚨\n\n"
                       f"🔥  {promotion_info['title']}  🔥\n\n"
                        f"💸  Preço: {promotion_info['price']}  💸")
            url_button = InlineKeyboardButton("Link para promoção", promotion_info["url"])
            inline_button = InlineKeyboardMarkup().add(url_button)
            
            sync_db.redis.lrem("unsent.promotions.id", 1, promotion_id)
            sync_db.redis.delete(f"promotion.{promotion_id}.info")
            
            for user_id in active_users_id:
                # tasks.append(asyncio.create_task(bot.bot.send_message(user_id, message, reply_markup=inline_button)))
                tasks.append(asyncio.create_task(bot.bot.send_photo(user_id, image, message, reply_markup=inline_button)))
            await asyncio.gather(*tasks)
    # TODO: remove this later        
    print(f"send_message - elapsed time = {timeit.default_timer() - start}")