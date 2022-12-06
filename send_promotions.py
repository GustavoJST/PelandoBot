from tgbot.utils.database import sync_db
import bot
import asyncio
import timeit

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
            message = (f"🔥 {promotion_info['title']} 🔥\n\n"
                        f"💸 Preço: {promotion_info['price']} 💸\n\n "
                        f"Link: {promotion_info['url']}")
            
            sync_db.redis.lrem("unsent.promotions.id", 1, promotion_id)
            sync_db.redis.delete(f"promotion.{promotion_id}.info")
            
            for user_id in active_users_id:
                tasks.append(asyncio.create_task(bot.bot.send_message(user_id, message)))
            await asyncio.gather(*tasks)
    # TODO: remove this later        
    print(f"send_message - elapsed time = {timeit.default_timer() - start}")