import psycopg2
import os

__connection = None


def get_connection():
    global db
    db = psycopg2.connect(
        dbname=os.environ['DB_NAME'],
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'],
        host=os.environ['DB_HOST'],
        port=os.environ['DB_PORT']
    )
    return db


def init_db(force: bool = True):
    conn = get_connection()
    c = conn.cursor()

    if force:
        c.execute('DROP TABLE IF EXISTS users CASCADE')
        c.execute('DROP TABLE IF EXISTS hotline')
        c.execute('DROP TABLE IF EXISTS links')
        c.execute('DROP TABLE IF EXISTS mails')
        c.execute('DROP TABLE IF EXISTS notifications')

    c.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id             int  primary key,
                    registration_date   text,
                    user_name           text,
                    group_name          text,
                    last_activity       text 
                )
            ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS hotline (
            user_id     int,
            subject     text not null,
            task        text not null,
            deadline    text not null,
            link        text,
            
            foreign key(user_id) references users(user_id)
        )
    ''')

    c.execute('''
            CREATE TABLE IF NOT EXISTS links (
                user_id      int,
                subject      text not null,
                subject_type text not null,
                link         text not null,
                password     text,
                description  text,

                foreign key(user_id) references users(user_id)
            )
        ''')

    c.execute('''
            CREATE TABLE IF NOT EXISTS mails (
                user_id     int,
                link        text not null,
                description text not null,
                
                foreign key(user_id) references users(user_id)
            )
    ''')

    c.execute('''
                CREATE TABLE IF NOT EXISTS notifications (
                    user_id     int,
                    cron_date        text not null,

                    foreign key(user_id) references users(user_id)
                )
        ''')

    conn.commit()

# working with users table


def users_register_user(user_id, registration_date: str, user_name: str, group_name: str, last_activity: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        'INSERT INTO users (user_id, registration_date, user_name, group_name, last_activity) VALUES (%s, %s, %s, %s, %s)',
        (user_id, registration_date, user_name, group_name, last_activity,)
    )
    conn.commit()


def users_update_group_name(user_id, user_name: str, group_name: str, last_activity: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        'UPDATE users SET user_name = %s, group_name = %s, last_activity = %s WHERE user_id = %s',
        (user_id, user_name, group_name, last_activity,)
    )
    conn.commit()


def users_update_last_activity(user_id, user_name: str, last_activity: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        'UPDATE users SET user_name = %s, last_activity = %s WHERE user_id = %s',
        (user_id, user_name, last_activity,)
    )
    conn.commit()


def add_hotline_with_link(user_id: int, subject: str, task: str, deadline: str, link: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        'INSERT INTO hotline (user_id, subject, task, deadline, link) VALUES (%s, %s, %s, %s, %s)',
        (user_id, subject, task, deadline, link,)
    )
    conn.commit()


def add_hotline_without_link(user_id: int, subject: str, task: str, deadline: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        'INSERT INTO hotline (user_id, subject, task, deadline) VALUES (%s, %s, %s, %s)',
        (user_id, subject, task, deadline,)
    )
    conn.commit()


def add_links(user_id: int, link: str, description: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        'INSERT INTO links (user_id, link, description) VALUES (%s, %s, %s)',
        (user_id, link, description,)
    )
    conn.commit()


def add_mails(user_id: int, link: str, description: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        'INSERT INTO mails (user_id, link, description) VALUES (%s, %s, %s)',
        (user_id, link, description,)
    )
    conn.commit()


def get_hotline_by_id(uid: int):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT subject, task, deadline, link FROM hotline WHERE user_id = %s', (uid,))

    return c.fetchall()


def get_links_by_id(uid: int):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT subject, subject_type, link, password, description FROM links WHERE user_id = %s', (uid,))

    return c.fetchall()


def get_mails_by_id(uid: int):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT link, description FROM mails WHERE user_id =%s', (uid,))

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


def get_user_by_id(uid: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE user_id = %s', (uid,))

    return c.fetchone()


def get_group_name_by_id(uid: int):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT group_name FROM users WHERE user_id = %s', (uid,))

    return c.fetchone()


def add_notification(uid: str, cron_date: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        'INSERT INTO notifications (user_id, cron_date) VALUES (%s, %s)',
        (uid, cron_date,)
    )
    conn.commit()
