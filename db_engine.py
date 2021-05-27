import sqlite3
from pathlib import Path


def sqlite_connect():
    conn = sqlite3.connect("data/database.db", check_same_thread=False)
    conn.execute("pragma journal_mode=wal;")
    return conn


def init_sqlite():
    conn = sqlite_connect()
    c = conn.cursor()
    c.execute('''CREATE TABLE users (id integer primary key, user_id integer, user_name text, user_surname text, 
    username text)''')
    c.execute('''CREATE TABLE portfolio (id integer primary key, stock_id integer, ticker text, 
    data text, price real, quantity real)''')
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
