from telegram.ext import Updater, CommandHandler, ConversationHandler, Filters
from telegram.ext.dispatcher import run_async
import threading
import queue

askers_lock = threading.Lock()
registrators_lock = threading.Lock()

askers = set()
registrators = set()

messages_queue = queue.Queue()

@run_async
def _help(bot, update):
    update.message.reply_text(
        'Hi, I am the bot that help to fastly find answers to your questions\n\n'\
        'Here is the test version, dont be rigorous.\n'\
        'First of all type */register* to register.\n'\
        'You can register as guest to ask questions or as local to answer them.\n'\
        'If you are guest and want to ask question, send */ask* before sending question.\n'\
        'Then you can send a question in one message and wait while smb will answer.\n'\
        'type */help* to see this message.'
        , parse_mode = 'Markdown')

# на question и регистрейшн асинк может и не нужен
# @run_async
def _question(bot, update):
    with askers_lock:
        askers.add(update.message.chat_id)

# @run_async
def _registration(bot, update):
    with registrators_lock:
        registrators.add(update.message.chat_id)

# @run_async
def _message_handler(bot, update):
    messages_queue.put((update.message.chat_id, update.message.text))


def main():
    token = '500529687:AAGE46fRiNB0JFveF_F6hphlrgsno6RGqto'
    updater = Updater(token)
    dp = updater.dispatcher

    help_handler = CommandHandler('help', _help)
    dp.add_handler(help_handler, group = 1)

    registration_handler = CommandHandler('register', _registration)
    dp.add_handler(registration_handler, group = 1)

    question_handler = CommandHandler('ask', _question)
    dp.add_handler(registration_handler, group = 0)

    message_handler = CommandHandler(Filters.text, _message_handler)
    dp.add_handler(message_handler, group = 0)


    # registration_handler = ConversationHandler(
    #     entry_points=[CommandHandler('register', self.registration())],
    #     states={
    #         LANGUAGE: [RegexHandler('^(English|Russian)$', self.language())],
    #         THEMES: [RegexHandler('^(IT|Physics)$', self.themes())]
    #     },
    #     fallbacks=[CommandHandler('cancel', self.cancel())]
    # )

if __name__ == '__main__':
    main()

