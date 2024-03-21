from .db import engine
from .models import User, Session
from sqlalchemy import select, insert, update, delete, and_, desc
from uuid import uuid4, UUID
from sqlalchemy.orm import joinedload


def create_session(username: str):
    with engine.connect() as conn:
        with conn.begin():
            conn.execute(insert(Session).values(username=username))

def is_loaded_image(username: str):
    with engine.connect() as conn:
        status = conn.execute(select(Session.loaded_image).where(Session.username == username)).scalar_one()
    if status is None:
        return False
    return status


def update_loaded_image(username: str, loaded_image: bool):
    with engine.connect() as conn:
        with conn.begin():
            conn.execute(update(Session).values(loaded_image=loaded_image).where(Session.username == username))
 