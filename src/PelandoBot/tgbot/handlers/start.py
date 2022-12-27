from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message
from pelandobot.tgbot.utils.database import async_db

async def start(message: Message, bot: AsyncTeleBot):
    if await async_db.redis.scard("active.chats.id") >= 1000 and not await async_db.redis.sismember("active.chats.id", message.chat.id):
        bot.send_message(message.chat.id, "Olá. Eu sou o PelandoBot, um bot não oficial do Pelando.\n\n" 
                           "Desculpe, mas não podemos incluir você na lista de membros pois ela está atualmente cheia.\n\n "
                           "Devido ao meu modo de operação, suporto apenas 1000 usuários simultâneos. "
                           "Tente novamente depois de algum tempo para checar se uma nova vaga foi liberada.")
        return
        
    await bot.send_message(message.chat.id, "Olá. Eu sou o PelandoBot, um bot de monitoramento de promoções não oficial do Pelando.\n\n"
                           "Sou um projeto open source. Você pode conferir meu código (não tão bonito) no link:\n"
                           "https://github.com/GustavoJST/PelandoBot\n\n" 
                           "Posso te ajudar encontrando, filtrando e te entregando as novas promoções "
                           "que surgirem no site do Pelando.\n\n"
                           "Eu possuo um sistema de tags similar a do Pelando, permitindo a você um melhor controle "
                           "sobre quais as promoções que devo lhe entregar. \n\n"
                           "Você pode conhecer mais sobre esse e outros sistemas "
                           "digitando\n/help.\n\n"
                           "Digite /promo para iniciar a busca por promoções e /tags para configurar "
                           "suas tags.")
  