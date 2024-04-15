from pathlib import Path
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
        authorization = request.authorization
        if authorization is None:
            raise html.P('unauthorized')#Exception('Login required')
        else:
            username = authorization['username']
            return func(username=username, *args, **kwargs)
        
    return wrapper



def register_admin():
    user_table.add_user(username='admin', password=Config.get_admin_password())

def register_local_user(username: str = 'local', password: str = '123'):
    user_table.add_user(username=username, password=password)

def register_users_from_csv(path_to_csv):
    if isinstance(path_to_csv, str):
        path_to_csv = Path(path_to_csv)
    if not not path_to_csv.exists():
        return
    df = pd.read_csv(path_to_csv, na_values='None', sep=';')
    for index, row in df.iterrows():
        name = row['name'] if pd.notna(row['name']) else None
        user_table.add_user(username=row['username'], password=row['password'], name=name) 


def start_sessions():
    users = user_table.get_users()
    for u in users:
        session_table.create_session(username=u.username)