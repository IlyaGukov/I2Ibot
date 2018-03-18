import threading
import queue
from ConversationThread import Conversation

LANGUAGES = frozenset(['English', 'Russian'])
THEMES = frozenset(['Physics', 'IT'])
conversaions = dict()

def process_conversation(message_chat_id_, message):
        # todo
    converstion = Conversation(message, message_chat_id)
    conversations[message_chat_id] = conversation
    conversation.main()

def process_registration(message_chat_id_, message_text_):
    if message_text_ in LANGUAGES:
        user_data_base.write_user_data(message_chat_id_, 'Languages', message_text_)
    elif message_text_ in THEMES:
        user_data_base.write_user_data(message_chat_id_, 'Themes', message_text_)

@run_async
def slow_message_processing(askers_table, registrators_table,
                            messages_queue, one_to_one):
    while True:
        message_chat_id, message_text = messages_queue.get()

        if one_to_one.search_and_pop():
            process_conversation(message_chat_id, message_text)

        elif askers_table.user_in_table(message_chat_id):
            proccess_conversation(message_chat_id, message_text)

        elif registrators_table.user_in_table(message_chat_id):
            process_registration(message_chat_id, message_text)
