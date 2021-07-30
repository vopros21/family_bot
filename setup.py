# external modules
import os
import telebot
from telebot import types

# internal modules
import quote_engine as qe
import portfolio_engine as pe
import db_engine as de

token = os.getenv('API_BOT_TOKEN')
bot = telebot.TeleBot(token)

# manual information argument
manual_flag = 'man'

commands = {
    'help': 'How to use the bot',
    'portfolio': 'Get portfolio statistics',
    'quote': 'Get a new smart quote',
    'save': 'Add new position into portfolio',
    'start': 'The most useful functionality'
}


def save_user_stat(message):
    us_id = int(message.from_user.id)
    us_name = message.from_user.first_name
    us_sname = message.from_user.last_name
    username = message.from_user.username
    current_date = int(message.date)
    query = message.text

    de.db_user_stat(user_id=us_id,
                    user_name=us_name,
                    user_surname=us_sname,
                    username=username,
                    current_date=current_date,
                    query=query
                    )


def manual(command):
    possible_answers = {
        'save': 'Command format "/save yyyy-mm-dd value quantity"\n'
                'Where value is a fractional number (0.0), quantity is a whole number (0)',
        'quote': 'Command format "/quote" or "/quote ru".'
                 'Returns some quote in Russian or English (by default)',
        'start': 'Lorem ipsum',
        'portfolio': 'Lorem ipsum'
    }
    try:
        return possible_answers[command]
    except KeyError as e:
        print(f'Manual request for wrong command: {command}\n', e)


@bot.message_handler(regexp='^.help')
def command_help_handler(message):
    """Method for getting some basic info about bot's functionality"""
    cid = message.chat.id
    text = '\n\t'.join(commands.keys())
    bot.send_message(cid, f'You can use the next commands:<b>\n\t{text}</b>\n'
                          f'For more information use "command man"', parse_mode='HTML')


@bot.message_handler(regexp='^.save')
def command_save_helper(message):
    """ Method for adding new shares into portfolio
        Query format "/save YYYY-MM-DD price quantity"
    """
    cid = message.chat.id
    manual_arg = 'save'
    if manual_flag in message.text:
        answer_text = manual(manual_arg)
    else:
        try:
            ticker, date, price, quantity = de.db_save_portfolio(user_text=message.text)
            answer_text = f"{quantity} shares for {ticker} with {price} was added to DB for {date}"
        except TypeError:
            answer_text = 'Error during saving process.'
    bot.send_message(cid, answer_text)


@bot.message_handler(commands=['start'])
def command_start_handler(message):
    cid = message.chat.id
    answer_text = 'Hello, user. I\'m glad to see you'
    manual_arg = 'start'
    if manual_arg in message.text:
        answer_text = manual(manual_arg)
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    bot.send_message(cid, answer_text, reply_markup=markup)


# Looks like quote API knows only EN and RU so only this two languages are supported
@bot.message_handler(commands=['quote'])
def command_quote_handler(message):
    cid = message.chat.id
    save_user_stat(message=message)
    manual_arg = 'quote'
    if manual_flag in message.text:
        answer_text = manual(manual_arg)
    else:
        message_list = message.text.split()
        quote_language = 'en'
        if len(message_list) > 1:
            quote_language = 'ru'
        quote, author = 'Quote', 'Author'
        answer_text = quote + " -" + author + "\n"
        try:
            quote, author = qe.get_quote(quote_language)
            quote = '<b>' + quote + '</b>'
            author = '<i>' + author + '</i>'
            answer_text = quote + "\n" + author
        except Exception as ex:
            print(ex)
    bot.send_message(cid, answer_text, parse_mode='HTML')


# TODO: add possibility to paint graph for portfolio
@bot.message_handler(regexp='^.portfolio')
def command_portfolio_handler(message):
    cid = message.chat.id
    save_user_stat(message=message)
    _, *symbols = message.text.split()
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    manual_arg = 'portfolio'
    if manual_flag in message.text:
        answer_text = manual(manual_arg)
    else:
        plvalue = 0
        tickers = ''
        if len(symbols) == 0:
            plvalue = pe.get_total_plvalue()
            tickers = 'all '
        else:
            for symbol in symbols:
                text_symbol = symbol.upper()
                plvalue = 0
                if de.is_stock_in_portfolio(text_symbol):
                    try:
                        plvalue += pe.get_plvalue(text_symbol)
                    except TypeError as e:
                        print(f'Wrong argument in db query {e}')
                tickers += f'{text_symbol} '
        if plvalue != 0:
            answer_text = f"This is your {tickers}profit/loss so far: {format(plvalue, '.2f')}"

        else:
            answer_text = 'Sorry. You don\'t have this instrument in your portfolio.'

    bot.send_message(cid, answer_text, reply_markup=markup)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
