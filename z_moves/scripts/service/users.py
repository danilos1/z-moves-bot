import z_moves.scripts.db as db
import time


def is_user_exists(user_id):
    user = db.get_user_by_id(user_id)
    return user is not None


def add_user(user_id, username, group):
    db.add_user(user_id, time.strftime('%d/%m/%y, %X'), username, group, time.strftime('%d/%m/%y, %X'))

def update_user(user_id, group):
    db.update_group(user_id, group, time.strftime('%d/%m/%y, %X'))
