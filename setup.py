import os
import quote_engine as qe
import portfolio_engine as pe
import db_engine as de

import telebot

from telebot import types

token = os.getenv('API_BOT_TOKEN')
bot = telebot.TeleBot(token)

known_users = []
user_steps = {}
commands = {
    'help': 'How to use the bot',
    'portfolio': 'Get portfolio statistics',
    'quote': 'Get a new smart quote',
    'start': 'The most useful functionality'
}


def save_user_stat(message):
    us_id = message.from_user.id
    us_name = message.from_user.first_name
    us_sname = message.from_user.last_name
    username = message.from_user.username
    current_date = message.date

    de.db_user_stat(user_id=us_id,
                    user_name=us_name,
                    user_surname=us_sname,
                    username=username,
                    current_date=current_date
                    )


@bot.message_handler(regexp='^.help')
def command_help_handler(message):
    cid = message.chat.id
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    bot.send_message(cid, 'This is a help message!', reply_markup=markup)
    print(message.text)


@bot.message_handler(regexp='^.save')
def command_save_helper(message):
    cid = message.chat.id
    ticker, date, price, quantity = message.text.split()
    # de.db_save_portfolio(ticker, date, price, quantity)
    de.db_read_users(2)
    # bot.send_message(cid, f"{quantity} shares for {ticker} with {price} was added to DB for {date}")


@bot.message_handler(commands=['start'])
def command_start_handler(message):
    cid = message.chat.id
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    bot.send_message(cid, 'Hello, user. I\'m glad to see you', reply_markup=markup)


# Looks like quote API knows only EN and RU so only this two languages are supported
@bot.message_handler(commands=['quote'])
def command_quote_handler(message):
    cid = message.chat.id
    save_user_stat(message=message)

    message_list = message.text.split()
    quote_language = 'en'
    if len(message_list) > 1:
        quote_language = 'ru'
    quote, author = 'Quote', 'Author'
    status = quote + " -" + author + "\n"
    try:
        quote, author = qe.get_quote(quote_language)
        quote = '<b>' + quote + '</b>'
        author = '<i>' + author + '</i>'
        status = quote + "\n" + author
    except Exception as ex:
        print(ex)
    bot.send_message(cid, status, parse_mode='HTML')


@bot.message_handler(regexp='^.portfolio')
def command_portfolio_handler(message):
    cid = message.chat.id
    save_user_stat(message=message)
    _, *symbols = message.text.split()
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    plvalue = 0
    tickers = ''
    if len(symbols) == 0:
        plvalue = pe.get_total_plvalue()
        tickers = 'all '
    else:
        for symbol in symbols:
            text_symbol = symbol.upper()
            plvalue += pe.get_plvalue(text_symbol)
            tickers += f'{text_symbol} '
    text = f"This is your {tickers}profit/loss so far: {format(plvalue, '.2f')}"
    if plvalue != 0:
        bot.send_message(cid, text, reply_markup=markup)
    else:
        bot.send_message(cid, 'Sorry. You don\'t have this instrument in your portfolio.', reply_markup=markup)


def morning_message():
    gid = -449881048
    quote, author = 'Quote', 'Author'
    status = quote + " -" + author + "\n"
    try:
        quote, author = qe.get_quote('ru')
        quote = '<b>' + quote + '</b>'
        author = '<i>' + author + '</i>'
        status = quote + "\n" + author
    except Exception as ex:
        print(ex)
    bot.send_message(gid, status, parse_mode='HTML')


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
