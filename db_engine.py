import re
import sqlite3
from pathlib import Path
import datetime
import market_data_engine as mde


# Main method to connect to DB
def sqlite_connect():
    conn = sqlite3.connect("data/database.db", check_same_thread=False)
    conn.execute("pragma journal_mode=wal;")
    return conn


def create_table_tickers(curs):
    curs.execute('''CREATE TABLE IF NOT EXISTS tickers (
        id integer primary key unique,
        ticker text unique
    )''')


def create_table_market_data_day(curs):
    curs.execute('''CREATE TABLE IF NOT EXISTS market_data_day (
        ticker_id integer,
        date integer,
        open real,
        high real,
        low real,
        close real,
        UNIQUE (ticker_id, date)
    )''')


def create_table_users(curs):
    curs.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id integer primary key unique,
        username text,
        user_name text,
        user_surname text
    )''')


def create_table_user_actions(curs):
    curs.execute('''CREATE TABLE IF NOT EXISTS user_actions (
        id integer primary key unique, 
        user_id integer, 
        date integer,
        user_query text
    )''')


def create_table_portfolio(curs):
    curs.execute('''CREATE TABLE IF NOT EXISTS portfolio (
        id integer primary key unique, 
        ticker_id integer, 
        date integer, 
        price real, 
        quantity real,
    )''')
# TODO: Add one more table to support add and subtract position in portfolio. Maybe a new table with total shares for
#  each stock and improve current portfolio table to support closed position (negative quantity??)


# Fill DB with USERS and PORTFOLIO tables
def init_sqlite():
    conn = sqlite_connect()
    c = conn.cursor()
    create_table_users(c)
    create_table_user_actions(c)
    create_table_portfolio(c)
    create_table_tickers(c)
    create_table_market_data_day(c)
    conn.commit()
    conn.close()
    return


# Creating DB for the first time
def create_db():
    try:
        init_sqlite()
    except Exception as e:
        print('Error while creating db: ', e.__repr__(), e.args)
        pass
    else:
        print('Success!')


# Connection to DB or creating a new one
db = Path("data/database.db")
try:
    db.resolve(strict=True)
except FileNotFoundError:
    print('Database not found. Trying to create a new one')
    create_db()


# Add user stat to db
def db_user_stat(user_id: int, user_name: str, user_surname: str, username: str, current_date: int, query: str):
    conn = sqlite_connect()
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (user_id, username, user_name, user_surname) VALUES (?, ?, ?, ?)',
                   (user_id, username, user_name, user_surname))
    cursor.execute('INSERT INTO user_actions (user_id, date, user_query) VALUES (?, ?, ?)',
                   (user_id, current_date, query))
    conn.commit()
    conn.close()


# Preparing portfolio data for saving
def validate_user_input(user_text):
    try:
        _, ticker, date, price, quantity = user_text.split()
    except ValueError:
        return None

    # check ticker format
    if not re.match('^[A-z]{2,4}$', ticker):
        return None
    else:
        ticker = ticker.upper()

    # check date format
    md_pair = {'01': 31,
               '02': 28,
               '03': 31,
               '04': 30,
               '05': 31,
               '06': 30,
               '07': 31,
               '08': 31,
               '09': 30,
               '10': 31,
               '11': 30,
               '12': 31}
    if not re.match('^20[0-9]{2}-[0-9]{2}-[0-9]{2}$', date)\
            or int(date.split('-')[1]) > 12\
            or int(date.split('-')[2]) > md_pair[date.split('-')[1]]:
        return None
    else:
        date = date.split('-')
        date = datetime.datetime(int(date[0]), int(date[1]), int(date[2]), 0, 0).timestamp()

    # check price format
    if not re.match('^[0-9]+[.]+[0-9]+$', price):
        return None
    else:
        price = float(price)

    # check quantity format
    if not re.match('^[0-9]+$', quantity):
        return None
    else:
        quantity = int(quantity)

    return ticker, date, price, quantity


def get_ticker_id(ticker, cursor):
    return cursor.execute(f'SELECT id FROM tickers WHERE ticker = ?', (ticker, )).fetchone()[0]


# Add new data to portfolio db
def db_save_portfolio(user_text):
    try:
        ticker, date, price, quantity = validate_user_input(user_text=user_text)
    except TypeError:
        return False
    conn = sqlite_connect()
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO tickers (ticker) VALUES (?)', (ticker, ))
    ticker_id = get_ticker_id(ticker, cursor)
    cursor.execute('INSERT INTO portfolio (ticker_id, date, price, quantity) VALUES (?, ?, ?, ?)',
                   (ticker_id, date, price, quantity))
    conn.commit()
    conn.close()
    date = str(datetime.datetime.fromtimestamp(date)).split()[0]
    return ticker, date, price, quantity


# Read data from USERS
def db_read_users(userid):
    conn = sqlite_connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (userid, ))
    print(cursor.fetchall())
    conn.close()


# Read portfolio from DB
def db_read_portfolio():
    connect = sqlite_connect()
    cursor = connect.cursor()
    cursor.execute('SELECT t.ticker, p.date, p.price, p.quantity '
                   'FROM tickers as t JOIN portfolio as p ON p.ticker_id = t.id')
    answer = cursor.fetchall()
    connect.close()
    return answer


def db_save_day_quote_record(ticker, d, o, h, low, c):
    conn = sqlite_connect()
    cursor = conn.cursor()
    ticker_id = get_ticker_id(ticker, cursor)
    cursor.execute('INSERT OR IGNORE INTO market_data_day (ticker_id, date, open, high, low, close) '
                   'VALUES (?, ?, ?, ?, ?, ?)', (ticker_id, d, o, h, low, c))
    conn.commit()
    conn.close()


def is_last_day_in_db(ticker):
    sec_in_day = 86400
    today = int(datetime.datetime.now().timestamp() // 100 * 100)
    conn = sqlite_connect()
    cursor = conn.cursor()
    ticker_id = get_ticker_id(ticker, cursor)
    last_day_in_db = cursor.execute('SELECT date from market_data_day WHERE ticker_id = ? '
                                    'ORDER BY date DESC LIMIT 1', (ticker_id, )).fetchone()
    if last_day_in_db is None:
        last_day_in_db = 0
    else:
        last_day_in_db = last_day_in_db[0]
    conn.close()
    return True if (today - last_day_in_db) < sec_in_day else False


def get_last_close_price(ticker):
    conn = sqlite_connect()
    cursor = conn.cursor()
    ticker_id = get_ticker_id(ticker, cursor)
    if not is_last_day_in_db(ticker):
        fresh_quotes = mde.get_ticker_quotes(ticker)
        for key in fresh_quotes.keys():
            o, h, low, c = fresh_quotes[key][0], fresh_quotes[key][1], fresh_quotes[key][2], fresh_quotes[key][3]
            db_save_day_quote_record(ticker, key, o, h, low, c)
    last_close = cursor.execute(f'SELECT close FROM market_data_day WHERE ticker_id =? '
                                f'ORDER BY date DESC LIMIT 1', (ticker_id, )).fetchone()[0]
    conn.close()
    return last_close


def is_stock_in_portfolio(ticker):
    return True if ticker in portfolio_tickers() else False


def portfolio_tickers():
    conn = sqlite_connect()
    cursor = conn.cursor()
    symbols = []
    for symbol in cursor.execute('SELECT ticker FROM tickers').fetchall():
        symbols.append(symbol[0])
    conn.close()
    return symbols


# method returning market data for specified symbol
def select_market_data(ticker: str, period: str):
    if not is_stock_in_portfolio(ticker):
        return None
    conn = sqlite_connect()
    cursor = conn.cursor()
    period_ago = get_date_period_ago(period)
    start_date = max(get_first_position_date(ticker, cursor)[0], period_ago)
    ticker_id = get_ticker_id(ticker, cursor)
    market_data_for_period = cursor.execute('SELECT date, close FROM market_data_day '
                                            'WHERE ticker_id = ? and date > ?', (ticker_id, start_date)).fetchall()
    conn.close()
    return market_data_for_period


# method returning the date of the first position
def get_first_position_date(ticker: str, cursor):
    """Get the opening date for the specified symbol"""
    ticker_id = get_ticker_id(ticker, cursor)
    position_dates = cursor.execute('SELECT date FROM portfolio WHERE ticker_id = ?', (ticker_id, )).fetchall()
    return min(position_dates)


# method returns the start date for specified period
def get_date_period_ago(period: str):
    """Get the beginning date for the specified period"""
    switch = {'1y': 365, '1m': 31, '1w': 7}
    if period not in switch:
        period = '1y'
    today = datetime.datetime.today()
    return int((today - datetime.timedelta(switch[period])).timestamp())


def get_buy_prices(ticker: str):
    """Get whole history for the specified symbol in the portfolio"""
    conn = sqlite_connect()
    cursor = conn.cursor()
    ticker_id = get_ticker_id(ticker, cursor)
    buy_prices = cursor.execute('SELECT date, price, quantity FROM portfolio WHERE ticker_id = ?',
                                (ticker_id, )).fetchall()
    conn.close()
    return buy_prices
