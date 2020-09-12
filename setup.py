import os
import json
import requests
import time

import telebot

from telebot import types

token = os.getenv('API_BOT_TOKEN')
bot = telebot.TeleBot(token)

known_users = []
user_steps = {}
commands = {
    'help': 'How to use the bot',
    'start': 'The most useful functionality'
}


def get_user_step(uid):
    if uid not in user_steps:
        known_users.append(uid)
        user_steps[uid] = 0
    else:
        user_steps[uid] += 1
    return user_steps[uid]


# TODO: Move quotes engine to different file
def get_quote():
    params = {
        'method': 'getQuote',
        'lang': 'en',
        'format': 'json'
    }
    res = requests.get('http://api.forismatic.com/api/1.0/', params)
    json_text = json.loads(res.text)
    return json_text["quoteText"], json_text["quoteAuthor"]


while True:
    try:
        quote, author = get_quote()
        status = quote+" -"+author+"\n"+"#python \
        #dailypython #twitterbot #pythonquotes #programming"
        print('\nUpdating : ', status)
        # api.update_status(status=status)
        print("\nGoing to Sleep for 1 min")
        time.sleep(60)
    except Exception as ex:
        print(ex)
        break


@bot.message_handler(commands=['start'])
def command_start_handler(message):
    cid = message.chat.id
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    bot.send_message(cid, 'Hello, user. I\'m glad to see you', reply_markup=markup)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
