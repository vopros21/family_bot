import os

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


@bot.message_handler(commands=['start'])
def command_start_handler(message):
    cid = message.chat.id
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    bot.send_message(cid, 'Hello, user. I\'m glad to see you', reply_markup=markup)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
