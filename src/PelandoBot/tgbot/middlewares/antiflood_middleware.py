from telebot.asyncio_handler_backends import BaseMiddleware
from telebot.async_telebot import CancelUpdate


class AntiFloodMiddleware(BaseMiddleware):
    def __init__(self, limit, bot) -> None:
        self.last_time: dict[int, int] = {}
        self.limit = limit
        # Always specify update types, otherwise middlewares won't work
        self.update_types = ['message']
        self.bot = bot

    async def pre_process(self, message, data):
        if message.text not in ["/start", "/stop", "/tags", "/spam", "/help", "/promo"]:
            return  # Make it work only for this command
        if message.from_user.id not in self.last_time:
            # User is not in a dict, so lets add and cancel this function
            self.last_time[message.from_user.id] = message.date
            return
        if message.date - self.last_time[message.from_user.id] < self.limit:
            # User is flooding
            await self.bot.send_message(message.chat.id, 'Beep boop. Você está mandando mensagens com muita frequência. Diminua o ritmo.')
            return CancelUpdate()
        # Write the time of the last request
        self.last_time[message.from_user.id] = message.date

    # Don't delete this or it'll raise NotImplementedError.
    async def post_process(self, message, data, exception):
        pass
