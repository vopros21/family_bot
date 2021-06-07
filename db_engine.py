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


# Add new data to portfolio db
def db_save_portfolio(ticker: str, date: str, price: float, quantity: float):
    conn = sqlite_connect()
    cursor = conn.cursor()
    stock_id = 0
    cursor.execute('INSERT INTO portfolio (stock_id, ticker, date, price, quantity) VALUES (?, ?, ?, ?, ?)',
                   (stock_id, ticker, date, price, quantity))
    conn.commit()
    conn.close()
    return None


# Read data from USERS
def db_read_users(userid):
    conn = sqlite_connect()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id={userid}")
    print(cursor.fetchall())
    conn.close()
