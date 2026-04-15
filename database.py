import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def init_db():
    conn = sqlite3.connect("creatix.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        topic TEXT,
        report TEXT,
        critic TEXT
    )
    """)

    conn.commit()
    conn.close()


def create_user(username, password):
    conn = sqlite3.connect("creatix.db")
    c = conn.cursor()

    try:
        hashed = hash_password(password)
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()


def login_user(username, password):
    conn = sqlite3.connect("creatix.db")
    c = conn.cursor()

    hashed = hash_password(password)
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed))
    user = c.fetchone()

    conn.close()
    return user


def save_history(username, topic, report, critic):
    conn = sqlite3.connect("creatix.db")
    c = conn.cursor()

    c.execute(
        "INSERT INTO history (username, topic, report, critic) VALUES (?, ?, ?, ?)",
        (username, topic, report, critic)
    )

    conn.commit()
    conn.close()


def get_history(username):
    conn = sqlite3.connect("creatix.db")
    c = conn.cursor()

    c.execute("SELECT topic, report, critic FROM history WHERE username=?", (username,))
    data = c.fetchall()

    conn.close()
    return data