from ..database import user_table, session_table
from flask import request
import pandas as pd
from ..config import Config
from dash import html



def get_users():
    user_pwd = {}
    users = user_table.get_users()
    for u in users:
        user_pwd[u.username] = u.password
    return user_pwd


def login_required(func: callable):
    def wrapper(*args, **kwargs):
        username = request.authorization['username']
        if username is None:
            raise html.P('unauthorized')#Exception('Login required')
        else:
            return func(username=username, *args, **kwargs)
        
    return wrapper



def register_admin():
    user_table.add_user(username='admin', password=Config.get_admin_password())

def register_users_from_csv(path_to_csv):
    df = pd.read_csv(path_to_csv, na_values='None', sep=';')
    for index, row in df.iterrows():
        name = row['name'] if pd.notna(row['name']) else None
        user_table.add_user(username=row['username'], password=row['password'], name=name) 


def start_sessions():
    users = user_table.get_users()
    for u in users:
        session_table.create_session(username=u.username)