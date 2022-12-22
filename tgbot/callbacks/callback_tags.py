import re
from telebot.async_telebot import AsyncTeleBot
from telebot.types import ForceReply, CallbackQuery, Message
from tgbot.states.register_state import UserStates
from tgbot.utils.database import async_db

async def tag_option_handler(call: CallbackQuery, bot: AsyncTeleBot):
    if await async_db.redis.exists(f"state.{call.message.chat.id}"):
        user_id = (await async_db.redis.get(f"state.{call.message.chat.id}")).split("\"")[1]
        user_name = (await bot.get_chat_member(call.message.chat.id, user_id)).user.full_name
        if user_name is None:
            user_name = "Usuário"

        await bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=[])
        
        if call.data == "exit":
            await async_db.redis.delete(f"state.{call.message.chat.id}")
            return
          
        if call.data == "add_tags":
            await bot.send_message(call.message.chat.id,
                                    "Regras para o uso de tags:\n\n"
                                    "1 - Digite as tags separando-as com virgula. Exemplo: Notebook, smartphone, amd\n\n"
                                    "2 - As tags podem ser digitadas em maiúsculo ou minúsculo.\n\n"
                                    "3 - O tamanho mínimo de uma tag é de 2 caracteres.\n\n"
                                    "4 - Faça o uso de acentos se necessário. Exemplo: Tênis, memória, ram \n\n"
                                    "5 - Lembre-se de digitar as tags corretamente. Evite erros como smartfone, notebok, etc.\n\n"
                                    "6 - Você pode usar no máximo 30 tags ao mesmo tempo.\n\n"
                                    "OBS: As tags seguem o mesmo sistema do pelando. "
                                    "Eu irei lhe entregar apenas promoções que tiverem em seu título uma das tags escolhidas.\n\n"
                                    "OBS²: Não seguir as regras acima fará com que você não receba promoções de forma correta "
                                    "ou não receba nenhuma promoção, até que se defina as tags de maneira correta.")
            
            await bot.set_state(user_id, UserStates.tags_add, call.message.chat.id)
            await async_db.redis.expire(f"state.{call.message.chat.id}", 180)
            await bot.send_message(call.message.chat.id, f"[{user_name}](tg://user?id={user_id}), digite quais tags você quer adicionar ou "
                                                         "digite /exit para sair.\n\n"
                                                         "Lembre-se, caso você digite uma tag que já exista na sua " 
                                                         "lista de tags, ela será ignorada.", parse_mode='Markdown', 
                                                          reply_markup=ForceReply(selective=True))
            return
            
        elif call.data == "remove_tags":
            user_tags =  await async_db.redis.smembers(f"tags.{call.message.chat.id}")
            if len(user_tags) == 0:
                await bot.send_message(call.message.chat.id, "Você não tem nenhuma tag para remover.")
                return

            await bot.set_state(user_id, UserStates.tags_remove, call.message.chat.id)
            await async_db.redis.expire(f"state.{call.message.chat.id}", 180)
            await bot.send_message(call.message.chat.id, f"[{user_name}](tg://user?id={user_id}), digite as tags que você quer remover ou digite /exit para sair.\n\n"
                                                         "OBS: Tags digitadas aqui e que não fazem parte da sua lista de tags atuais serão ignoradas.", 
                                                        reply_markup=ForceReply(), parse_mode='Markdown')
            return
        
        elif call.data == "clean_tags":
            await async_db.redis.delete(f"state.{call.message.chat.id}")
            if not await async_db.redis.exists(f"tags.{call.message.chat.id}"):
                await bot.send_message(call.message.chat.id, "Não há tags para serem limpas.")
                return
            
            await async_db.redis.delete(f"tags.{call.message.chat.id}")
            await bot.send_message(call.message.chat.id, "Tags limpas com sucesso. "
                                                         "Você receberá todas as novas promoções a partir de agora.")
            return
        

async def handle_tags_input(message: Message, bot: AsyncTeleBot):
    if message.text == "/exit":
        await async_db.redis.delete(f"state.{message.chat.id}")
        await bot.reply_to(message, "Saída efetuada com sucesso!")
        return
    
    user_state = await async_db.redis.get(f"state.{message.chat.id}")
    user_state = user_state.split("\"")[5].split(":")[1]
    teste = await bot.get_state(message.from_user.id, message.chat.id)
    
    # User reply state key in db has expired.
    if user_state == None:
        await bot.send_message(message.chat.id, "Tempo limite para a configuração de tags atingido. "
                               "Digite /tags novamente para reiniciar o processo.")
        await async_db.redis.delete(f"state.{message.chat.id}")
        return
    
    # First regex checks if the tags follow the [tag, tag, tag] message pattern and 
    # the second regex checks for single character words/digits, to exclude things like [tag, a, b, tag].
    # Because of that, it enforces a 2 character minimum limit for user tags.
    if not re.search("(?i)^[a-zà-ãç-íò-õù-ú0-9\ ,]+$", message.text) or re.search("(^|\s|\,)\w(\s|\,|$)", message.text):
        await bot.reply_to(message, "Suas tags não seguem o padrão necessário. "
                           "Lembre-se, você não pode usar caracteres especiais além dos acentos/vírgulas e "
                           "o limite mínimo de caracteres para uma tag é de 2 caracteres. "
                           "Siga o exemplo abaixo.\n\n"
                           "Exemplo: Tênis, memória, ram, moletom, nike\n\n"
                           "Digite suas tags novamente ou digite /exit para sair da definição de tags.")
        return
    
    input_tags = set(message.text.replace(" ", "").lower().split(","))
    input_tags.discard("")
    db_tags =  await async_db.redis.smembers(f"tags.{message.chat.id}")
 
    if user_state == "tags_add":
        add_tags_difference = input_tags.difference(db_tags)
        if not add_tags_difference:
            await bot.reply_to(message, "Todas as tags digitadas já estão presentes na sua lista de tags atuais. "
                                    "Digite novas tags diferentes das que você já tem ou digite /exit para sair.")
            return
        
        if (len(add_tags_difference) + len(db_tags)) > 30:
            await bot.reply_to(message, "Você está ultrapassando o limite de 30 tags. "
                                                f"Você tem {30 - (len(db_tags))} tag(s) restante(s) para digitar "
                                                f"e sua mensagem contém {len(input_tags)} tag(s).\n\n"
                                                "Por favor, remova algumas tags da mensagem e digite-as novamente ou digite "
                                                "/exit para sair.")
            return
        
        await async_db.redis.sadd(f"tags.{message.chat.id}", *add_tags_difference)
        await bot.reply_to(message, f"Operação concluída. {len(add_tags_difference)} tag(s) definida(s) com sucesso e "
                                    f"{len(input_tags) - len(add_tags_difference)} tag(s) ignorada(s).")
        await async_db.redis.delete(f"state.{message.chat.id}")
    
    elif user_state == "tags_remove":
        rem_tags_difference = input_tags.intersection(db_tags)
        if not rem_tags_difference:
            await bot.reply_to(message, "Nenhuma das tags digitadas está presente nas suas tags atuais. Digite novamente ou "
                               "digite /exit para sair.")
            return
            
        await async_db.redis.srem(f"tags.{message.chat.id}", *rem_tags_difference)
        await bot.send_message(message.chat.id, f"Operação concluída. {len(rem_tags_difference)} tag(s) removida(s) com sucesso e "
                                                f"{len(input_tags) - len(rem_tags_difference)} tag(s) ignorada(s).")
        await async_db.redis.delete(f"state.{message.chat.id}")