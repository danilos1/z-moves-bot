import sqlite3

__connection = None


def get_connection():
    global __connection
    if __connection is None:
        __connection = sqlite3.connect('z-moves.db', check_same_thread=False)
    return __connection


def init_db(force: bool = False):
    conn = get_connection()
    c = conn.cursor()

    if force:
        c.execute('DROP TABLE IF EXISTS hotline')

    c.execute('''
        CREATE TABLE IF NOT EXISTS hotline (
            subject     text not null,
            task        text not null,
            deadline    date,
            link        text
        )
    ''')

    conn.commit()


def add_hotline(subject: str, task: str, deadline, link:str):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        'INSERT INTO hotline (subject, task, deadline, link) VALUES (?, ?, ?, ?)',
        (subject, task, deadline, link)
    )

def get_all_hotlines():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM hotline')

    return c.fetchall()


if __name__ == '__main__':
    init_db()
    add_hotline("AK-2", 'Lab5', '011.13.20', 'somelink')
    print(get_all_hotlines())