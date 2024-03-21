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


def is_start_annotation(username: str) -> bool:
    with engine.connect() as conn:
        status = conn.execute(select(Session.start_annotation).where(Session.username == username)).scalar_one()
    if status is None:
        return False
    return status


def get_selected_class(username: str) -> int:
    with engine.connect() as conn:
        selected_class = conn.execute(select(Session.selected_class).where(Session.username == username)).scalar_one()
    return selected_class


def get_save_path(username: str) -> str:
    with engine.connect() as conn:
        save_path = conn.execute(select(Session.save_path).where(Session.username == username)).scalar_one()
    return save_path


def update_loaded_image(username: str, loaded_image: bool):
    with engine.connect() as conn:
        with conn.begin():
            conn.execute(update(Session).values(loaded_image=loaded_image).where(Session.username == username))
 
 
def update_start_annotation(username: str, start_annotation: bool):
    with engine.connect() as conn:
        with conn.begin():
            conn.execute(update(Session).values(start_annotation=start_annotation).where(Session.username == username))
            
            
def update_selected_class(username: str, selected_class: int):
    with engine.connect() as conn:
        with conn.begin():
            conn.execute(update(Session).values(selected_class=selected_class).where(Session.username == username))
            
def update_save_path(username: str, save_path: str):
    with engine.connect() as conn:
        with conn.begin():
            conn.execute(update(Session).values(save_path=save_path).where(Session.username == username))