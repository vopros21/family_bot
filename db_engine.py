import re
import sqlite3
from pathlib import Path


# Main method to connect to DB
def sqlite_connect():
    conn = sqlite3.connect("data/database.db", check_same_thread=False)
    conn.execute("pragma journal_mode=wal;")
    return conn


# Fill DB with USERS and PORTFOLIO tables
def init_sqlite():
    conn = sqlite_connect()
    c = conn.cursor()
    c.execute('''CREATE TABLE users (
        id integer primary key autoincrement, 
        user_id integer, 
        user_name text, 
        user_surname text, 
        username text,
        date text
    )''')
    c.execute('''CREATE TABLE portfolio (
        id integer primary key autoincrement, 
        stock_id integer, 
        ticker text, 
        date text, 
        price real, 
        quantity real
    )''')
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
def db_user_stat(user_id: int, user_name: str, user_surname: str, username: str, current_date: str):
    conn = sqlite_connect()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (user_id, user_name, user_surname, username, date) VALUES (?, ?, ?, ?, ?)',
                   (user_id, user_name, user_surname, username, current_date))
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


# Find ticker id to use for saving
def db_get_ticker_id(ticker):
    conn = sqlite_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM portfolio")
    db_port = cursor.fetchall()
    conn.close()
    max_id = 0
    for line in db_port:
        if line[1] > max_id:
            max_id = line[1]
        if line[2] == ticker:
            return line[1]
    return max_id + 1


# Add new data to portfolio db
def db_save_portfolio(user_text):
    try:
        ticker, date, price, quantity = validate_user_input(user_text=user_text)
    except TypeError:
        return False
    conn = sqlite_connect()
    cursor = conn.cursor()
    stock_id = db_get_ticker_id(ticker=ticker)
    cursor.execute('INSERT INTO portfolio (stock_id, ticker, date, price, quantity) VALUES (?, ?, ?, ?, ?)',
                   (stock_id, ticker, date, price, quantity))
    conn.commit()
    conn.close()
    return ticker, date, price, quantity


# Read data from USERS
def db_read_users(userid):
    conn = sqlite_connect()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id={userid}")
    print(cursor.fetchall())
    conn.close()


# Read portfolio from DB
def db_read_portfolio():
    connect = sqlite_connect()
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM portfolio")
    answer = cursor.fetchall()
    connect.close()
    return answer
