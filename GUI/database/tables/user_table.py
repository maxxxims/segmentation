from ..db import engine
from ..models import User
from sqlalchemy import select, insert, update, delete, and_, desc
from uuid import uuid4, UUID
from sqlalchemy.orm import joinedload


def add_user(username: str, password: str, name = None):
    data = {'username': username, 'password': password}
    if name is not None:
        data['name'] = name
    with engine.connect() as conn:
        with conn.begin():
            conn.execute(insert(User).values(**data))


def get_users():
    with engine.begin() as conn:
        result = conn.execute(select(User))
    return result.all()