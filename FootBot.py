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

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

waiting = 1

def gen_params_geocode(city):
    params = {
        'format': 'json',
        'kind': 'locality',
        'geocode': city,
        'key': 'AArKKloBAAAAeL7SagIBohUyX2O1S-2BJ8ctwvi2Lld9ehUAAAAAAAAAAADxbezDgQnrTHgYFVdqLQE6ilgwIQ=='
    }
    return params

def gen_params_owm(lat, lon):
    params = {
        'lat': str(lat),
        'lon': str(lon),
        'lang': 'ru',
        'APPID': 'd37e83b57e323f22cd8e0c0766b408e9'
    }
    return params

def gen_params_poem(weather):
    weather = weather.replace(' ', '+')
    params = {
        'query': weather,
    }
    return params

def gen_params_pict(city, weather):
    if (weather == 'грусть'):
        q = weather
    else:
        q = weather + '+декабрь+' + city

    params = {
        'q': q,
        'tbm': 'isch'
    }
    return params

def getTranslation(text):
    params = {
        'lang': 'ru-en',
        'key': 'trnsl.1.1.20171120T234144Z.0f8a4fc2a302c8a5.1692e34778a68d52577ebf77648c0bb64c1d37e4',
        'text': text
    }
    url = 'https://translate.yandex.net'
    command = '/api/v1.5/tr.json/translate'
    header = {'Content-Type': 'application/x-www-form-urlencoded'}

    try:
        tr = requests.post(url+command, params = params,  headers = header)
        return tr.json()['text'][0]
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print (e)
        return ''
    
    return tr.json()['text'][0]

def clean_city_name(city, rubbish):
    
    pattern = '^' + rubbish + ' '
    m = re.match(pattern, city)
    while (m != None):
        city = city[m.end():]
        m = re.match(pattern, city)

    pattern = ' ' + rubbish + ' '
    m = re.search(pattern, city)
    while (m != None):
        city = city[:m.start() + 1] + city[m.end():]
        m = re.search(pattern, city)

    pattern = ' ' + rubbish + '$'
    m = re.search(pattern, city)
    while (m != None):
        city = city[:m.start()]
        m = re.match(pattern, city)

    return city

def parse_user_request(user_req):
    
    words_to_replace = ["погода", "погоды", "погоду", "погоде", "какая", "weather", "what",
        "прогноз", "forecast", ".", ",", "!", "?"]
    user_req = user_req.lower()
    for word in words_to_replace:
        user_req = user_req.replace(word, '')
    user_req = user_req.strip()

    today = datetime.datetime.today()
    city = user_req
    
    answer = list()

    if 'послезавтра' in user_req:
        answer.append(today + datetime.timedelta(days=2))
        city = city.replace('послезавтра', '')

    for word in user_req.split():
        a = parse(word, languages=['ru'], settings={'PREFER_DATES_FROM': 'future', 'TIMEZONE': 'UTC+3'})
        if (a != None):
            answer.append(a)
            city = city.replace(word, '')

    if (len(answer) == 0):
        user_req_en = getTranslation(user_req)
        pattern = '[а-я]'
        if (len(re.findall(pattern, user_req)) == 0):
            city = user_req_en
        
        for word in user_req_en.split():
            a = parse(word, languages=['en'], settings={'PREFER_DATES_FROM': 'future', 'TIMEZONE': 'UTC+3'})
            if (a != None):
                answer.append(a)
                city = city.replace(word, '')

    if (len(answer) != 0):
        date = sorted(answer)[0]
    else:
        date = today

    rubbish_names = ['в', 'на', 'in', 'on', 'is', 'с', 'среду', 'пятницу',
        'субботу', 'что', 'подскажи', 'знаешь', 'бро', 'брат', 'for', 'числа', 'декабря']
    for rub in rubbish_names:
        city = clean_city_name(city, rub)

    if ((date.day - today.day >= 5) or (date.day - today.day < 0)):
        date = False

    return city.strip(), date

def gen_weather_string(data, city, date):

    if (city == False):
        return data, 'грусть'

    answer = 'Привет, Бро! Помогу чем могу.\n\n'
    answer += 'Нашел: ' + city + ' (' + str(date.date()) + ')' +'\n'
    answer += '*' + data['weather'][0]['description'].capitalize() + '*\n'
    # answer += 'Подробнее:\n'
    answer += '{0:{fill}{align}15}'.format('`Температура', fill='.', align='<')
    if (data['main']['temp_min'] != data['main']['temp_max']):
        temp_min = int(data['main']['temp_min'] - 273)
        temp_max = int(data['main']['temp_max'] - 273)
        answer += 'от ' + str('+' if (temp_min > 0) else '') + str(temp_min) +\
            ' до ' + str('+' if (temp_max > 0) else '') + str(temp_max) + ' ℃`\n'
    else:
        temp_min = int(data['main']['temp_min'] - 273)
        answer += str('+' if (temp_min > 0) else '') + str(temp_min) + ' ℃`\n'

    answer += '{0:{fill}{align}15}'.format('`Ветер', fill='.', align='<') + \
        str(data['wind']['speed']) + ' м/с`\n'
    answer += '{0:{fill}{align}15}'.format('`Давление', fill='.', align='<') + \
        str(int(float(data['main']['pressure'])*0.750062)) + ' мм рт.ст.`\n'
    answer += '{0:{fill}{align}15}'.format('`Влажность', fill='.', align='<') + \
        str(data['main']['humidity']) + ' %`\n'
    
    return answer, data['weather'][0]['description']

def req_weather(city, date):
    url = 'https://geocode-maps.yandex.ru/1.x/'
    req_geocode = requests.get(url, params = gen_params_geocode(city))
    if (len(req_geocode.json()['response']['GeoObjectCollection']['featureMember']) > 0):
        lon, lat = req_geocode.json()['response']['GeoObjectCollection']['featureMember'][0]\
            ['GeoObject']['Point']['pos'].split()
        city = req_geocode.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['name']
    else:
        lon, lat = 0, 0
        city = False
    
    if (city != False):
        today = datetime.datetime.today()
        url = 'http://api.openweathermap.org/data/2.5/'
        if (date.date() == datetime.datetime.today().date()):
            command = 'weather'
        else:
            command = 'forecast'

        header = {'Content-Type': 'application/x-www-form-urlencoded'}
        req_owm = requests.post(url+command, params = gen_params_owm(lat, lon),  headers = header)

        if (date.date() == datetime.datetime.today().date()):
            return gen_weather_string(req_owm.json(), city, date)
        else:
            weather_data =  False
            for result in req_owm.json()['list']:
                if (result['dt_txt'] == str(date.date()) + ' 15:00:00'):
                    weather_data = result
            if (weather_data != False):
                return gen_weather_string(weather_data, city, date)

    return gen_weather_string('Извини, Брат, не получилось.', False, date)

def req_picture(city, weather):
    url = 'https://www.google.ru/'
    command = 'search'
    header = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64)\
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
    
    req = requests.get(url+command, headers = header, params = gen_params_pict(city, weather))
    soup = BeautifulSoup(req.text, 'lxml')
    length = len(soup.findAll('div', attrs = {'class': 'rg_meta notranslate'}))
    if (length > 0):
        length = 5 if (length > 5) else length
        picture_url = json.loads(soup.findAll('div', attrs = {'class': 'rg_meta notranslate'})
                                 [np.random.randint(length)].contents[0])['ou']
    else:
        picture_url = False
    return picture_url

def req_poems(weather):
    url = 'http://poetory.ru/content/'
    command = 'list'
    header = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64)\
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
    if (weather == 'ясно'):
    	weather += ' солнце'

    zaglushka = '''Играя в недоношенные чувства,
Признав любовь заглушкой пустоты,
Срезаю с неё левые болты.

Душевно лапая дешёвое искусство,
Задёргивая шторой небеса,
Разбавив звук и выключив глаза.

Где страх съедается, личинкой буквоблудства,
Сминая годы в скороточное мгновенье,
Поймав его, как ветра дуновенье.

Но, сшив из занавесок паруса,
Не заработав ни имён и ни имений,
Так и не выбрав ни дорог, ни направлений.

Наведываюсь прямо в небеса,
Туда, где радуги цветная полоса.'''
    
    try:
        req = requests.get(url+command, params = gen_params_poem(weather), timeout=10)
        soup = BeautifulSoup(req.text, 'lxml')
        poems = soup.findAll('div', attrs = {'class': 'item-text-share hidden'})    
        
        if (len(poems) > 0):
            return poems[np.random.randint(len(poems))].getText()
        else:
            req = requests.get(url+command, params = gen_params_poem(weather.split()[-1]), timeout=10)
            soup = BeautifulSoup(req.text, 'lxml')
            poems = soup.findAll('div', attrs = {'class': 'item-text-share hidden'})
            if (len(poems) > 0):
                return poems[np.random.randint(len(poems))].getText()
            else:
                req = requests.get(url+command, params = gen_params_poem('костыль'), timeout=10)
                soup = BeautifulSoup(req.text, 'lxml')
                poems = soup.findAll('div', attrs = {'class': 'item-text-share hidden'})
                if (len(poems) > 0):
                    return poems[np.random.randint(len(poems))].getText()
                else:
                    return zaglushka

    except requests.exceptions.RequestException as e:
        return 'Брат, стишок не грузится, извини.'
def help(bot, update):
    update.message.reply_text(
        'Привет!\n'
        'Я погодный *Бро*Бот, надеюсь мы подружимся!\n'
        '\n'
        'Меня можно спрашивать про погоду в любых городах на сегодня и ближайшие *5 дней*.\n'
        'Я понимаю по-русски и немного по-английски, отвечаю только по-русски.\n'
        'У меня есть некоторые проблемы с пониманием чисел прописью, так что давай лучше цифрами.\n'
        '\n'
        'Примеры запросов:\n'
        '[Владивосток]\n'
        '[погода в Москве]\n'
        '[какая погода в Сан-Франциско завтра]\n'
        '[Казань в Четверг]'
        , parse_mode = 'Markdown')

def send_weather(bot, update):

    bot.send_chat_action(chat_id=update.message.chat_id, action = ChatAction.TYPING)
    city, date = parse_user_request(update.message.text)
    if (date == False):
        answer = 'Брат, походу с датой проблема, проверь.\n'\
        'Я ищу погоду только на сегодня и 5 ближайших дней.'
        weather = 'грусть'
    else:
        bot.send_chat_action(chat_id=update.message.chat_id, action = ChatAction.TYPING)
        answer, weather = req_weather(city, date)
    bot.send_chat_action(chat_id=update.message.chat_id, action = ChatAction.TYPING)
    photo = req_picture(city, weather)
    bot.send_chat_action(chat_id=update.message.chat_id, action = ChatAction.TYPING)
    poem = req_poems(weather)

    print(city,date)
    print(answer)

    bot.send_message(chat_id=update.message.chat_id, text = answer, parse_mode = 'Markdown')

    bot.send_chat_action(chat_id=update.message.chat_id, action = ChatAction.UPLOAD_PHOTO)
    if (photo != False):
        bot.send_photo(chat_id=update.message.chat_id, photo = photo)
    else:
        bot.send_photo(chat_id=update.message.chat_id, photo = open('fail.jpg', 'rb'))
    bot.send_message(chat_id=update.message.chat_id, text = poem)


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Удачи, Брат.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the EventHandler and pass it your bot's token.
    token = '509338032:AAFeU7Mewmc5SMQ6HWW3cB3IwfpwENPq9xw'
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    start_handler = CommandHandler('start', help)
    dp.add_handler(start_handler)
    help_handler = CommandHandler('help', help)
    dp.add_handler(help_handler)
    cancel_handler = CommandHandler('cancel', cancel)
    dp.add_handler(cancel_handler)
    weather_request_handler = MessageHandler(Filters.text, send_weather)
    dp.add_handler(weather_request_handler)


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