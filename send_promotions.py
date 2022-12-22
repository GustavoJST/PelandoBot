import bot
import traceback
import asyncio
import timeit
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from tgbot.utils.database import sync_db

def prepare_process():
    asyncio.run(send_message())


async def send_message():
    start = timeit.default_timer()
    while sync_db.redis.exists("unsent.promotions.id"):
        tasks = set()
        # TODO: Remove this later
        start = timeit.default_timer()
        active_chats_id = sync_db.redis.smembers("active.chats.id")
        unsent_promotions = sync_db.redis.lrange("unsent.promotions.id", 0, -1)
       
        for promotion_id in unsent_promotions:
            promotion_info = sync_db.redis.hgetall(f"promotion.{promotion_id}.info")
            try:
                image = promotion_info["image"]
                message = (f"🚨  PROMOÇÃO  🚨\n\n"
                            f"🔥  {promotion_info['title']}  🔥\n\n"
                            f"💸  Preço: {promotion_info['price']}  💸")
            except KeyError:
                with open("./logfile.txt","a", encoding="utf-8") as logfile:
                    logfile.write(traceback.format_exc())
                    logfile.write(f"\n Additional info: \n {promotion_info}")
                    logfile.write("\n\n\n\n")
                    print("\n\nException Logged Successfully!\n\n")
                    continue

            url_button = InlineKeyboardButton("Link para promoção", promotion_info["url"])
            inline_button = InlineKeyboardMarkup().add(url_button)
    
            active_chats_id_tmp = list(active_chats_id.copy())
            while len(active_chats_id_tmp) != 0:
                # TODO: Como iterar através dos usuários, sem repetir, 25 de cada vez?
                for chat_id in active_chats_id_tmp:
                    if len(tasks) == 25:
                        break
                    
                    active_chats_id_tmp.remove(chat_id)
                    
                    if sync_db.redis.exists(f"tags.{chat_id}"):
                        if not sync_db.redis.sinter(f"tags.{chat_id}", f"promotion.{promotion_id}.tags"):
                            continue
                        
                    tasks.add(asyncio.create_task(bot.bot.send_photo(chat_id, image, message, reply_markup=inline_button)))
                    
                while tasks:
                    # TODO :Se começar a surgir vários erros, o programa ira esperar 1 seg pra cada erro = demorado.
                    # talvez mudar de FIRST_EXCEPTION para ALL_COMPLETED, assim aumentando a eficiência.
                    start_asyncio = timeit.default_timer()
                    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION)
                    print(f"asyncio.wait - elapsed time = {timeit.default_timer() - start_asyncio}")
        
                    for task in done:
                        tasks.remove(task)
                        if task.exception() is not None:
                            if task._exception.error_code == 400:
                                tasks.add(asyncio.create_task(bot.bot.send_message(chat_id, 
                                                                                   message, 
                                                                                   reply_markup=inline_button)))
                                logfile.write(traceback.format_exc(task._exception))
                                logfile.write(f"\n Additional info: \n {promotion_info}")
                                logfile.write("\n\n\n\n")
                                print("\n\nException Logged Successfully!\n\n")
                                    
                            elif task._exception.error_code == 429:
                                tasks.add(asyncio.create_task(bot.bot.send_photo(chat_id, 
                                                                                 image, 
                                                                                 message, 
                                                                                 reply_markup=inline_button)))
                            else:
                                with open("./logfile.txt","a", encoding="utf-8") as logfile:
                                    logfile.write(traceback.format_exc(task._exception))
                                    logfile.write(f"\n Additional info: \n {promotion_info}")
                                    logfile.write("\n\n\n\n")
                                    print("\n\nException Logged Successfully!\n\n")
                                    
                    # Limits the message sent rate so it doesn't trigger 429 errors.               
                    await asyncio.sleep(1.2)
                                         
            sync_db.redis.lrem("unsent.promotions.id", 1, promotion_id)
            sync_db.redis.delete(f"promotion.{promotion_id}.info")       
            sync_db.redis.delete(f"promotion.{promotion_id}.tags")
            
    # TODO: remove this later        
    print(f"send_message - elapsed time = {timeit.default_timer() - start}")