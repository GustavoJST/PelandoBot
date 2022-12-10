from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

async def start(message: Message, bot: AsyncTeleBot):
    await bot.send_message(message.chat.id, "Beep boop. Eu sou o PelandoBot. Um bot não oficial do Pelando.\n\n" 
                           "Vou te ajudar encontrando, filtrando e te entregando as novas promoções "
                           "que surgirem no site do Pelando.\n\n"
                           "Eu possuo um sistema de tags similar a do Pelando, permitindo a você um melhor controle "
                           "sobre quais as promoções que devo lhe entregar. \n\n"
                           "Você pode conhecer mais sobre esse e outros sistemas "
                           "digitando /help.")
  