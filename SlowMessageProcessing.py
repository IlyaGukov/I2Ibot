import threading
import queue
from ConversationThread import Conversation

# todo
conversation_object = 0
conversaions = {'asker_chat_id', conversation_object}

def process_conversation(message_chat_id_, message):
	converstion = Conversation(message, message_chat_id)
	conversation[message_chat_id] = conversation
	conversation.main()

    # todo

def process_registration(message_chat_id_, message_text_):
    # todo

@run_async
def slow_message_processing(askers_lock, askers, 
                            registrators_lock, registrators,
                            messages_queue, one_to_one):
    while True:
        message_chat_id, message_text = messages_queue.get()

        if one_to_one.search_and_pop():
            process_conversation(message_chat_id, message_text)

        else:
            askers_lock.acquire()
            try:
                if message_chat_id in askers:
                    askers_lock.release()
                    proccess_conversation(message_chat_id, message_text)
            finally:
                askers_lock.release()

            registrators_lock.acquire()
            try:
                if message_chat_id in registrators:
                    registrators_lock.release()
                    proccess_registration(message_chat_id, message_text)
            finally:
                registrators_lock.release()

        