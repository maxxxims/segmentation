from ..database import user_table
from flask import request


def get_users():
    user_pwd = {}
    users = user_table.get_users()
    for u in users:
        user_pwd[u.username] = u.password
    print(user_pwd)
    return user_pwd



def login_required(func: callable):
    def wrapper(*args, **kwargs):
        username = request.authorization['username']
        if username is None:
            raise Exception('Login required')
        else:
            return func(username=username, *args, **kwargs)
        
    return wrapper