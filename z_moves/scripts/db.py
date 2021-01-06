import postgresql
import psycopg2
import os

__connection = None


def get_connection():
    global db
    db = psycopg2.connect(dbname=os.environ['DB_NAME'], user=os.environ['DB_USERNAME'], password=os.environ['DB_PASSWORD'], host=os.environ['DB_HOST'], port=os.environ['DB_PORT'])
    return db



def init_db(force: bool = False):
    conn = get_connection()
    c = conn.cursor()

    if force:
        c.execute('DROP TABLE IF EXISTS users CASCADE ')
        c.execute('DROP TABLE IF EXISTS hotline')
        c.execute('DROP TABLE IF EXISTS links')

    c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id     int  primary key
            )
        ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS hotline (
            user_id     int,
            subject     text not null,
            task        text not null,
            deadline    date not null,
            link        text,
            
            foreign key(user_id) references users(user_id)
        )
    ''')

    c.execute('''
            CREATE TABLE IF NOT EXISTS links (
                user_id      int,
                link         text not null,
                description  text not null,

                foreign key(user_id) references users(user_id)
            )
        ''')

    conn.commit()

def add_user(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        'INSERT INTO users (user_id) VALUES (%s)',
        (user_id,)
    )
    conn.commit()

def add_hotline(user_id: int, subject: str, task: str, deadline, link:str):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        'INSERT INTO hotline (user_id, subject, task, deadline, link) VALUES (?, ?, ?, ?, ?)',
        (user_id, subject, task, deadline, link)
    )

def add_hotline_without_link(user_id: int, subject: str, task: str, deadline):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        'INSERT INTO hotline (user_id, subject, task, deadline) VALUES (?, ?, ?, ?)',
        (user_id, subject, task, deadline)
    )

def add_links(user_id: int, link: str, description: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        'INSERT INTO links (user_id, link, description) VALUES (?, ?, ?)',
        (user_id, link, description)
    )

def get_hotline_by_id(uid: int):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT subject, task, deadline, link FROM hotline WHERE user_id = ?', (uid,))

    return c.fetchall()

def get_links_by_id(uid: int):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT link, description FROM links WHERE user_id = ?', (uid,))

    return c.fetchall()

def get_all_hotlines():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT user_id, subject, task, deadline, link FROM hotline')

    return c.fetchall()

def get_all_users():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT user_id FROM users')

    return c.fetchall()
