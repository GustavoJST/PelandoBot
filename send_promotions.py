import bot
import traceback
import asyncio
import timeit
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from tgbot.utils.database import sync_db

def prepare_process():
    asyncio.run(send_message())


async def task_scheduler(tasks, chat_id, message, button, image=None, last_retry=False):
    if image != None:
        tasks[asyncio.create_task(bot.bot.send_photo(chat_id, image, message, reply_markup=button))] = chat_id, image, message, button, last_retry
    else:
        tasks[asyncio.create_task(bot.bot.send_message(chat_id, message, reply_markup=button))] = chat_id, image, message, button, last_retry


async def send_message():
    start = timeit.default_timer()
    while sync_db.redis.exists("unsent.promotions.id"):
        tasks = dict()
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
                url_button = InlineKeyboardButton("Link para promoção", promotion_info["url"])
                inline_button = InlineKeyboardMarkup().add(url_button)
            except KeyError:
                with open("./logfile.txt", "a", encoding="utf-8") as logfile:
                    logfile.write(traceback.format_exc())
                    logfile.write(f"\n Additional info: \n {promotion_info}")
                    logfile.write("\n\n\n\n")
                    print("\n\nException Logged Successfully!\n\n")
                    continue

            active_chats_id_tmp = active_chats_id.copy()
            chats_to_remove = set()
            while len(active_chats_id_tmp) != 0:
                for chat_id in active_chats_id_tmp:
                    if len(tasks) == 25:
                        break
                    
                    chats_to_remove.add(chat_id)
                    if sync_db.redis.exists(f"tags.{chat_id}"):
                        if not sync_db.redis.sinter(f"tags.{chat_id}", f"promotion.{promotion_id}.tags"):
                            continue
                        
                    await task_scheduler(tasks, chat_id, message, inline_button, image)           
                    
                [active_chats_id_tmp.discard(chat) for chat in chats_to_remove]   
                 
                start_asyncio = timeit.default_timer()
                # TODO: Talvez seja mais eficiente usar ALL_COMPLETED ao invés de FIRST_EXCEPTION
                done, pending = await asyncio.wait(tasks.keys(), return_when=asyncio.ALL_COMPLETED)
                print(f"asyncio.wait - elapsed time = {timeit.default_timer() - start_asyncio}")
    
                for task in done: 
                    if task.exception() is not None:
                        logfile = open("./logfile.txt", "a", encoding="utf-8")
                        # TODO: Colocar o primeiro if como erro 429 e o restante cair num else.
                        if task._exception.error_code == 400:
                            re_chat_id, re_image, re_message, re_button, last_retry = tasks.pop(task)
                            if last_retry != True:
                                await task_scheduler(tasks, re_chat_id, re_message, re_button, last_retry=True) 

                                
                        elif task._exception.error_code == 429:
                            re_chat_id, re_image, re_message, re_button, last_retry = tasks.pop(task)
                            await task_scheduler(tasks, re_chat_id, re_message, re_button, re_image)
                            logfile.write(f"\n Status 429 error - Rescheduling task... \n {promotion_info}")
                            
                        else:
                            logfile.write(traceback.format_exc(task._exception()))
                            logfile.write(f"\n Unkown error - Additional info: \n {promotion_info}")
                            logfile.write("\n\n\n\n")
                            print("\n\nException logged successfully!\n\n")
                        logfile.close()
                                    
                # Limits the message sent rate so it doesn't trigger 429 errors.               
                await asyncio.sleep(2)
                                         
            sync_db.redis.lrem("unsent.promotions.id", 1, promotion_id)
            sync_db.redis.delete(f"promotion.{promotion_id}.info")       
            sync_db.redis.delete(f"promotion.{promotion_id}.tags")
            
    # TODO: Remove this later        
    print(f"send_message - elapsed time = {timeit.default_timer() - start}")