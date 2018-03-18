import threading
import queue
from ConversationThread import Conversation

conversaions = dict()

def process_conversation(message_chat_id_, message):
	converstion = Conversation(message, message_chat_id)
	conversations[message_chat_id] = conversation
	conversation.main()

    # todo

def process_registration(message_chat_id_, message_text_):
    
    # todo

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

