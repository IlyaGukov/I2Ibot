import threading
import logging
import queue
from DBase import UserDataBase, One_to_one
from ConversationThread import Conversation
from telegram.ext.dispatcher import run_async
from telegram import ReplyKeyboardMarkup

logging.basicConfig(format='SMP(%(asctime)s - %(name)s - %(levelname)s - %(message)s):',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


@run_async
def slow_message_processing(bot, askers_table, registrators_table, messages_queue):

    # probably not good idea
    LANGUAGES = frozenset(['English', 'Russian'])
    THEMES = frozenset(['Physics', 'IT'])
    user_data_base = UserDataBase()
    one_to_one = One_to_one()
    conversaions = dict()

    def _process_conversation(message_chat_id_, message, new_conversation):
            # todo
        if new_conversation:
            logger.info("Conversation with question '%s' started by chat_id: '%d'", message, message_chat_id_)
            converstion = Conversation(message, message_chat_id)
            conversations[message_chat_id] = conversation
            conversation.main()
        else:
            logger.info("Old conversation is processed with answer '%s'", message)

    def _process_registration(message_chat_id_, message_text_):
        if message_text_ in LANGUAGES:
            reply_keyboard = [THEMES]
            bot.send_message(chat_id = message_chat_id_,
                text = 'Which topics do you know?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            user_data_base.write_user_data(message_chat_id_, 'Languages', message_text_)

        elif message_text_ in THEMES:
            user_data_base.write_user_data(message_chat_id_, 'Themes', message_text_)
            logger.info("User %d removed from registrators_table", message_chat_id_)
            registrators_table.remove_user(message_chat_id_)

        else:
            reply_keyboard = [LANGUAGES]
            bot.send_message(chat_id = message_chat_id_,
                text = 'Which languages do you know?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            user_data_base.add_user(message_chat_id_, message_text_)

    while True:
        message_chat_id, message_text = messages_queue.get()

        if one_to_one.search_and_pop(message_chat_id):
            _process_conversation(message_chat_id, message_text, new_conversation = False)

        elif askers_table.user_in_table(message_chat_id):
            _proccess_conversation(message_chat_id, message_text, new_conversation = True)

        elif registrators_table.user_in_table(message_chat_id):
            _process_registration(message_chat_id, message_text)
