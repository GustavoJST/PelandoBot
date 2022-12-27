from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message


async def help(message: Message, bot: AsyncTeleBot):
    await bot.send_message(message.chat.id, parse_mode="HTML",
                           text="<b>O que eu posso fazer por você:</b>\n\n"
                           "* Entregar novas promoções assim que elas aparecerem no site do Pelando.\n\n"
                           "* Filtrar as novas promoções, entregando apenas as relevantes para você através do sistema de Tags.\n\n"
                           "<b>O que são tags?</b>\n\n"
                           "Tags são palavras-chave que são usadas para filtrar promoções. "
                           "No site do Pelando, você tem a opção de escolher tags para receber novos alertas referentes as tags escolhidas.\n"
                           "Por exemplo, ao escolher a tag 'notebook', você irá receber uma notificação do aplicativo do Pelando para "
                           "cada promoção que tiver notebook no título, não importando modelo, marca, cor, etc.\n\n"
                           "O mesmo acontece para mim, escolha uma ou mais tags, e quando aparecer uma promoção que tenha, "
                           "em seu título, uma das tags que você escolheu, eu irei lhe avisar mandando uma mensagem.\n\n"
                           "<b>Por quanto tempo minhas tags ficam guardadas?</b>\n\n"
                           "Suas tags ficam guardadas desde que você esteja me utilizando. Entretanto, ao digitar /stop "
                           "para finalizar minha execução, irei guardar as suas tags por exatamente dois meses, para caso "
                           "você queira meus serviços novamente.\nPassado esse tempo, suas tags serão deletadas automaticamente, e "
                           "será necessário reconfigurá-las novamente utilizando o comando /tags.\n\n"
                           "<b>Configurei minhas tags mas não estou recebendo nenhuma promoção. O que eu faço?</b>\n\n"
                           "Duas coisas podem estar acontecendo:\n\n"
                           "1 - Você configurou as tags de forma certa, porém deu azar de nenhuma promoção ter aparecido ainda. "
                           "Isso é mais comum do que parece, além de ser algo que não tem como resolver a não ser esperar.\n\n"
                           "2 - Você configurou as tags de forma errada, sendo provavelmente algum erro ortográfico "
                           "ou sua tag é uma palavra que não existe.\n\n"
                           "Digite /tags novamente para analisar quais as suas tags atuais, e remova-as/adicione-as novamente se necessário.")

    await bot.send_message(message.chat.id, parse_mode="HTML",
                           text="<b> Por que há um limite de apenas 1000 chats/usuários para o bot? </b>\n\n"
                           "Infelizmente, o Telegram possui um limite na quantidade de requisições que podem ser feita aos seus "
                           "servidores em um determinado espaço de tempo. Atualmente, esse limite é de 30 requisições (envios de mensagem) "
                           "por segundo, o que torna a tarefa de mandar promoções atualizadas algo difícil, pois quanto mais usuários, "
                           "maior será o delay entre uma nova promoção surgir e eu entregar a notificação para você.\n\n"
                           "Um jeito eficiente de contornar este problema é me adicionar a um grupo. Dessa forma, eu consigo alcançar um público "
                           "maior enviando apenas uma notificação, ao invés de notificar cada usuário separadamente por mensagens privadas.\n\n"
                           "<b>OBS</b>: Apenas administradores/donos de grupos podem interagir comigo através dos comandos.\n\n"
                           "<b>Adicionei o bot no meu canal mas ele não responde aos comandos. O que eu faço?</b>\n\n"
                           "Infelizmente, não funciono em canais, apenas em grupos ou chats privados.\n\n"
                           "<b>Sou administrador/dono de um grupo mas o bot não responde aos comandos.</b>\n\n"
                           "Infelizmente, não consigo responder a comandos de administradores/donos anônimos. "
                           "Desative a opção 'Permanecer anônimo' nas configurações dos administradores do grupo.")
