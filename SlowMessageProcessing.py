import threading
import logging
import queue
from ConversationThread import Conversation

logging.basicConfig(format='SMP(%(asctime)s - %(name)s - %(levelname)s - %(message)s):',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

LANGUAGES = frozenset(['English', 'Russian'])
THEMES = frozenset(['Physics', 'IT'])
conversaions = dict()

def process_conversation(message_chat_id_, message, new_conversation):
        # todo
    if new_conversation:
        logger.info("Conversation with question '%s' started by chat_id: ", message)    #todo add chat_id to logger
        converstion = Conversation(message, message_chat_id)
        conversations[message_chat_id] = conversation
        conversation.main()
    else:
        logger.info("Old conversation is processed with answer '%s'", message)

def process_registration(message_chat_id_, message_text_):
    if message_text_ in LANGUAGES:
        user_data_base.write_user_data(message_chat_id_, 'Languages', message_text_)
    elif message_text_ in THEMES:
        user_data_base.write_user_data(message_chat_id_, 'Themes', message_text_)
        logger.info("User %d removed from registrators_table", message_chat_id_)
        registrators_table.remove_user(message_chat_id_)

@run_async
def slow_message_processing(bot, askers_table, registrators_table,
                            messages_queue, one_to_one):
    while True:
        message_chat_id, message_text = messages_queue.get()

        if one_to_one.search_and_pop():
            process_conversation(message_chat_id, message_text, new_conversation = False)

        elif askers_table.user_in_table(message_chat_id):
            proccess_conversation(message_chat_id, message_text, new_conversation = True)

        elif registrators_table.user_in_table(message_chat_id):
            process_registration(message_chat_id, message_text)
