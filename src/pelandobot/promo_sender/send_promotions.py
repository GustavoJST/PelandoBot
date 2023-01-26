import pelandobot.app.bot as bot
import traceback
import asyncio
import timeit
import time
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from pelandobot.tgbot.utils.database import sync_db


async def func_loop():
    while True:
        time.sleep(2)
        if sync_db.redis.exists("unsent.promotions.id"):
            await send_message()


async def delete_promotion(promotion_id):
    sync_db.redis.lrem("unsent.promotions.id", 1, promotion_id)
    sync_db.redis.delete(f"promotion.{promotion_id}.info")
    sync_db.redis.delete(f"promotion.{promotion_id}.tags")


async def task_scheduler(tasks, chat_id, message, button, image=None, last_retry=False):
    if image is not None:
        tasks[asyncio.create_task(bot.bot.send_photo(chat_id, image, message, reply_markup=button))] = (
            chat_id,
            image,
            message,
            button,
            last_retry,
        )
    else:
        tasks[asyncio.create_task(bot.bot.send_message(chat_id, message, reply_markup=button))] = (
            chat_id,
            image,
            message,
            button,
            last_retry,
        )


async def send_message():
    start = timeit.default_timer()
    while sync_db.redis.exists("unsent.promotions.id"):
        tasks = dict()
        active_chats_id = sync_db.redis.smembers("active.chats.id")
        unsent_promotions = sync_db.redis.lrange("unsent.promotions.id", 0, -1)

        for promotion_id in unsent_promotions:
            promotion_info = sync_db.redis.hgetall(f"promotion.{promotion_id}.info")
            try:
                image = None if promotion_info["image"] == "" else promotion_info["image"]
                message = (
                    f"🚨  PROMOÇÃO  🚨\n\n"
                    f"🔥  {promotion_info['title']}  🔥\n\n"
                    f"💸  Preço: {promotion_info['price']}  💸"
                )
                url_button = InlineKeyboardButton("Link para promoção", promotion_info["url"])
                inline_button = InlineKeyboardMarkup().add(url_button)
            except KeyError as e:
                with open("./logfile.txt", "a", encoding="utf-8") as logfile:
                    logfile.write(f"\nKeyError:\n{str(e)}")
                    logfile.write(f"\nAdditional info:\n {promotion_info}")
                    logfile.write("\n\n\n\n")
                    print("\n\nException Logged Successfully!\n\n")
                    await delete_promotion(promotion_id)
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
                done, pending = await asyncio.wait(tasks.keys(), return_when=asyncio.ALL_COMPLETED)
                print(f"asyncio.wait - elapsed time = {timeit.default_timer() - start_asyncio}")

                for task in done:
                    if task.exception() is not None:
                        logfile = open("./logfile.txt", "a", encoding="utf-8")
                        # Bad request. Caused by image URL not being supported by Telegram.
                        # Only one attempt to resend the message is made when this error occurs.
                        if task._exception.error_code == 400:
                            re_chat_id, re_image, re_message, re_button, last_retry = tasks.pop(task)
                            if not last_retry:
                                await task_scheduler(
                                    tasks, re_chat_id, re_message, re_button, last_retry=True
                                )

                        # Too many requests.
                        # Keeps rescheduling the task until it successfully finishes.
                        elif task._exception.error_code == 429:
                            re_chat_id, re_image, re_message, re_button, last_retry = tasks.pop(task)
                            await task_scheduler(tasks, re_chat_id, re_message, re_button, re_image)
                            logfile.write(
                                f"\n Status 429 error - Rescheduling task... \n {promotion_info}"
                            )

                        # Forbidden. User either blocked the bot or kicked the bot from the group before
                        # typing /stop to stop the bot.
                        # User is removed from the database.
                        elif task._exception.error_code == 403:
                            re_chat_id, re_image, re_message, re_button, last_retry = tasks.pop(task)
                            sync_db.remove_user(re_chat_id)

                        # Unknown error. Logs the error to a file for future debuging.
                        # TODO: Remove this later.
                        else:
                            traceback_string = "".join(traceback.format_exception(task.exception()))
                            logfile.write(f"\nERROR:\n{traceback_string}")
                            logfile.write(f"\nAdditional info:\n{promotion_info}")
                            logfile.write("\n\n\n\n")
                            print("\n\nException logged successfully!\n\n")
                            tasks.pop(task)
                        logfile.close()

                    tasks.pop(task)
                # Limits the message sent rate so it doesn't trigger 429 errors.
                await asyncio.sleep(2)

            await delete_promotion(promotion_id)

    # TODO: Remove this later
    print(f"send_message - elapsed time = {timeit.default_timer() - start}")


if __name__ == "__main__":
    asyncio.run(func_loop())
