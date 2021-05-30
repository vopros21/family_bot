import sqlite3
from pathlib import Path


def sqlite_connect():
    conn = sqlite3.connect("data/database.db", check_same_thread=False)
    conn.execute("pragma journal_mode=wal;")
    return conn


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


def create_db():
    try:
        init_sqlite()
    except Exception as e:
        print('Error while creating db: ', e.__repr__(), e.args)
        pass
    else:
        print('Success!')


db = Path("data/database.db")
try:
    db.resolve(strict=True)
except FileNotFoundError:
    print('Database not found. Trying to create a new one')
    create_db()


def db_table_val(user_id: int, user_name: str, user_surname: str, username: str, current_date: str):
    conn = sqlite_connect()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (user_id, user_name, user_surname, username, date) VALUES (?, ?, ?, ?)',
                   (user_id, user_name, user_surname, username, current_date))
    conn.commit()
