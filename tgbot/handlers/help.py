from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

async def help(message: Message, bot: AsyncTeleBot):
    await bot.send_message(message.chat.id, "Olá. Eu sou o PelandoBot, Um bot de promoções não oficial do Pelando.\n\n" 
                           "Sou um projeto de código aberto. Você pode conferir meu código no link:\n"
                           "https://github.com/GustavoJST/PelandoBot\n\n\n"
                           "O que eu posso fazer por você:\n"
                           "* Entregar novas promoções assim que elas aparecerem no site do Pelando.\n"
                           "* Filtrar as novas promoções, entregando apenas as relevantes para você através do sistema de Tags.\n\n"
                           "O que são tags?\n"
                           "Tags são palavras-chave que são usadas para filtrar promoções. "
                           "No site do Pelando, você tem a opção de escolher tags para receber novos alertas referentes as tags escolhidas.\n"
                           "Por exemplo, ao escolher a tag 'notebook', você irá receber uma notificação do aplicativo do Pelando para "
                           "cada promoção que tiver notebook no título, não importando modelo, marca, cor, etc.\n\n"
                           "O mesmo acontece para mim, escolha uma ou mais tags, e quando aparecer uma promoção que tenha, "
                           "em seu título, uma das tags que você escolheu, eu irei lhe avisar mandando uma mensagem.\n\n"
                           "Por quanto tempo minhas tags ficam guardadas?\n"
                           "Suas tags ficam guardadas desde que você esteja me utilizando. Entretanto, ao digitar /stop "
                           "para finalizar minha execução, irei guardar as suas tags por exatamente dois meses, para caso "
                           "você queira meus serviços novamente.\nPassado esse tempo, suas tags serão deletadas automaticamente, e "
                           "será necessário reconfigurá-las novamente utilizando o comando /tags.\n\n"
                           "Configurei minhas tags mas não estou recebendo nenhuma promoção. O que eu faço?\n"
                           "Duas coisas podem estar acontecendo:\n"
                           "1 - Você configurou as tags de forma certa, porém deu azar de nenhuma promoção ter aparecido ainda. "
                           "Isso é mais comum do que parece, além de ser algo que não tem como resolver a não ser esperar.\n"
                           "2 - Você configurou as tags de forma errada, sendo provavelmente algum erro ortográfico "
                           "ou sua tag é uma palavra que não existe.\n"
                           "Digite /tags novamente para analisar quais as suas tags atuais, e remova-as/adicione-as novamente se necessário.")
    
