from telegram.ext import Updater, CommandHandler, ConversationHandler, Filters
from telegram.ext.dispatcher import run_async
from UserTable import UserTable
import threading
import logging
import queue

# Enable logging
logging.basicConfig(format='FMP(%(asctime)s - %(name)s - %(levelname)s - %(message)s):',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

askers_table = UserTable()
registrators_table = UserTable()

messages_queue = queue.Queue()

@run_async
def _help(bot, update):
    update.message.reply_text(
        'Hi, I am the bot that help to fastly find answers to your questions\n\n'\
        'Here is the test version, dont be rigorous.\n'\
        'First of all type */register* to register.\n'\
        'You can add more languages/themes using */edit_profile* \n'\
        'If you want to ask question, send */ask* before sending question.\n'\
        'Then you can send a question in one message and hope that smb will answer.\n'\
        'type */help* to see this message.'
        , parse_mode = 'Markdown')

@run_async
def _send_error(message_chat_id_, error_message):
    bot.send_message(chat_id=message_chat_id_, text = error_message, parse_mode = 'Markdown')

# на question и регистрейшн асинк может и не нужен
# @run_async
def _question(bot, update):
    if registrators_table.user_in_table(update.message.chat_id):
        _send_error(update.message.chat_id,
            'please end registration/profile_data_correction process before asking questions')
    else:
        logger.info("User %d added to askers_table", update.message.chat_id)
        askers_table.add_user(update.message.chat_id)

# @run_async
def _registration(bot, update):
    logger.info("User %d added to registrators_table", update.message.chat_id)
    registrators_table.add_user(update.message.chat_id)

# @run_async
def _message_handler(bot, update):
    messages_queue.put((update.message.chat_id, update.message.text))

def main():
    token = ''
    updater = Updater(token)
    dp = updater.dispatcher

    help_handler = CommandHandler('help', _help)
    dp.add_handler(help_handler, group = 1)

    registration_handler = CommandHandler('register', _registration)
    dp.add_handler(registration_handler, group = 1)

    registration_handler = CommandHandler('edit_profile', _registration)
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

