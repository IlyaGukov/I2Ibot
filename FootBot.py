#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This Bot uses the Updater class to handle the bot.

First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

"""

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ChatAction)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
from bs4 import BeautifulSoup
from dateparser import parse
import datetime
import numpy as np
import requests
import json
import logging
import re
from user import User
from ListOfAnswerers import ListOfAnswerers
from ListOfRequests import ListOfRequests
from request import Request

NUMBER_OF_ANSWERS_TO_SEND = 1
NUMBER_OF_DODIKS_TO_ASK = 1

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

Counter = 0

LANGUAGE, THANKS = range(2)
QUESTION = range(1)

list_of_answerer = ListOfAnswerers()
list_of_requests = ListOfRequests()

temp = [1,2] #это заглушка
users_guest = [] #этотоже
users_local = []

# def getTranslation(text):
#     params = {
#         'lang': 'ru-en',
#         'key': 'trnsl.1.1.20171120T234144Z.0f8a4fc2a302c8a5.1692e34778a68d52577ebf77648c0bb64c1d37e4',
#         'text': text
#     }
#     url = 'https://translate.yandex.net'
#     command = '/api/v1.5/tr.json/translate'
#     header = {'Content-Type': 'application/x-www-form-urlencoded'}

#     try:
#         tr = requests.post(url+command, params = params,  headers = header)
#         return tr.json()['text'][0]
#     except requests.exceptions.RequestException as e:  # This is the correct syntax
#         print (e)
#         return ''
    
#     return tr.json()['text'][0]


# def send_weather(bot, update):

#     bot.send_chat_action(chat_id=update.message.chat_id, action = ChatAction.TYPING)
#     city, date = parse_user_request(update.message.text)
#     if (date == False):
#         answer = 'Брат, походу с датой проблема, проверь.\n'\
#         'Я ищу погоду только на сегодня и 5 ближайших дней.'
#         weather = 'грусть'
#     else:
#         bot.send_chat_action(chat_id=update.message.chat_id, action = ChatAction.TYPING)
#         answer, weather = req_weather(city, date)
#     bot.send_chat_action(chat_id=update.message.chat_id, action = ChatAction.TYPING)
#     photo = req_picture(city, weather)
#     bot.send_chat_action(chat_id=update.message.chat_id, action = ChatAction.TYPING)
#     poem = req_poems(weather)

#     print(city,date)
#     print(answer)

#     bot.send_message(chat_id=update.message.chat_id, text = answer, parse_mode = 'Markdown')

#     bot.send_chat_action(chat_id=update.message.chat_id, action = ChatAction.UPLOAD_PHOTO)
#     if (photo != False):
#         bot.send_photo(chat_id=update.message.chat_id, photo = photo)
#     else:
#         bot.send_photo(chat_id=update.message.chat_id, photo = open('fail.jpg', 'rb'))
#     bot.send_message(chat_id=update.message.chat_id, text = poem)


def help(bot, update):
    update.message.reply_text(
        'type /register to register\n'\
        'type /ask <question>, to send request to locals\n'\
        'type /help for this message'
        , parse_mode = 'Markdown')

def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Удачи, Брат.',
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def send_advert(bot):
    answer = '*ADVERTISMENT:*\n'\
    'Come to I2I, realize your ideas'
    for user in users_local:
        bot.send_message(chat_id=user.get_chat_id, text = answer, parse_mode = 'Markdown')
        bot.send_photo(chat_id=user.get_chat_id, photo = open('advert.jpg', 'rb'))
    for user in users_local:
        bot.send_message(chat_id=user.get_chat_id, text = answer, parse_mode = 'Markdown')
        bot.send_photo(chat_id=user.get_chat_id, photo = open('advert.jpg', 'rb'))

def create_request(bot, update):
    Counter += 1
    if ((counter // 5) == 0):
        send_advert(bot)

    req = Request(bot, update.message.chat_id, update.message.text)
    list_of_requests.add_request(update.message.chat_id, req)
    arr_of_asked = req.ask_dodiks(NUMBER_OF_DODIKS_TO_ASK, users_local) #todo: import array_of_all
    for asked in arr_of_asked:
        list_of_answerer.add_to_answerer(answerer_id = asked.get_chat_id(), who_ask = update.message.chat_id)

    return ConversationHandler.END

def registration(bot, update):
    reply_keyboard = [['Guest', 'Russian_local']]

    update.message.reply_text(
        'Hi! Are you FWC guest or local?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return LANGUAGE


def languages(bot, update):
    reply_keyboard = [['English', 'Spanish']]

    temp[0] = update.message.text #это заглушка
    if (temp[0] == 'Guest'):
        update.message.reply_text(
            'Which language do you speak?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    elif(temp[0] == 'Russian_local'):
        update.message.reply_text(
            'Which language do you know additionaly to russian?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return THANKS


def thanks(bot, update):
    if (temp[0] == 'Guest'):
        users_guest.append(User(temp[0], update.message.text, update.message.chat_id))
        update.message.reply_text('Thanks, now you can ask locals with /ask command')

    else:
        users_local.append(User(temp[0], update.message.text, update.message.chat_id))
        update.message.reply_text('wait, guests will come soon!')

    return ConversationHandler.END


def question(bot, update):
    update.message.reply_text('Now, ask question in one message please')
    return QUESTION


def process_answer(bot, update):
    answerer_id = update.message.chat_id
    if list_of_answerer.contain(answerer_id):
        asker_id = list_of_answerer.get_first_asker(answerer_id)
        list_of_answerer.remove_from_answerer(answerer_id, asker_id)
        if list_of_requests.contain(asker_id):
            req = list_of_requests.get_request(asker_id)
            req.add_answer(update.message.from_user.first_name, update.message.text)
            if (req.number_of_answers == NUMBER_OF_ANSWERS_TO_SEND):
                list_of_requests.remove_from_requests(asker_id)
                req.send_answers()
        else:
            print ('no request from this asker')
    else:
        print('no requests for this answerer')


def main():
    # Create the EventHandler and pass it your bot's token.
    token = '500529687:AAGE46fRiNB0JFveF_F6hphlrgsno6RGqto'
    updater = Updater(token)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    print('here am i')
    start_handler = CommandHandler('start', help)
    dp.add_handler(start_handler)

    help_handler = CommandHandler('help', help)
    dp.add_handler(help_handler)

    registration_handler = ConversationHandler(
        entry_points=[CommandHandler('register', registration)],

        states={
            LANGUAGE: [RegexHandler('^(Guest|Russian_local)$', languages)],

            THANKS: [RegexHandler('^(English|Spanish)$', thanks)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(registration_handler)

    question_handler = ConversationHandler(
        entry_points=[CommandHandler('ask', question)],

        states={
            QUESTION: [MessageHandler(Filters.text, create_request)],
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(question_handler)

    answer_handler = MessageHandler(Filters.text, process_answer)
    dp.add_handler(answer_handler)

    cancel_handler = CommandHandler('cancel', cancel)
    dp.add_handler(cancel_handler)



    # weather_request_handler = MessageHandler(Filters.text, ask_local)
    # dp.add_handler(weather_request_handler)


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