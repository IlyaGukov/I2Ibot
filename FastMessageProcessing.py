from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from telegram.ext.dispatcher import run_async
from telegram import ReplyKeyboardMarkup
from UserTable import UserTable
from DBase import One_to_one
from SlowMessageProcessing import slow_message_processing
import threading
import logging
import queue

# Enable logging
logging.basicConfig(format='SMP:    %(asctime)s - %(name)s - %(levelname)s - %(message)s',
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
@run_async
def _question_asked(bot, update):
    if registrators_table.user_in_table(update.message.chat_id):
        _send_error(update.message.chat_id,
            'please end registration/profile_data_correction process before asking questions')
    else:
        logger.info("User %d added to askers_table", update.message.chat_id)
        askers_table.add_user(update.message.chat_id)
        update.message.reply_text('Now, ask question in one message please')

@run_async
def _registration(bot, update):
    logger.info("User %d added to registrators_table", update.message.chat_id)
    #ToDo probably speaking to all registrators should be in separate thread
    registrators_table.add_user(update.message.chat_id)
    update.message.reply_text('What is your name?')

# @run_async
def _message_handler(bot, update):
    messages_queue.put((update.message.chat_id, update.message.text))

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def main():
    token = ''
    updater = Updater(token)
    dp = updater.dispatcher

    slow_message_processing(dp.bot, askers_table, registrators_table, messages_queue)

    help_handler = CommandHandler('start', _help)
    dp.add_handler(help_handler, group = 1)

    help_handler = CommandHandler('help', _help)
    dp.add_handler(help_handler, group = 1)

    registration_handler = CommandHandler('register', _registration)
    dp.add_handler(registration_handler, group = 1)

    registration_handler = CommandHandler('edit_profile', _registration)
    dp.add_handler(registration_handler, group = 1)

    question_handler = CommandHandler('ask', _question_asked)
    dp.add_handler(question_handler, group = 0)

    message_handler = MessageHandler(Filters.text, _message_handler)
    dp.add_handler(message_handler, group = 0)


    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()

