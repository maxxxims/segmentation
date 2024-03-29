from ..db import engine
from ..models import User, Session
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

def get_show_polygons(username: str) -> bool:
    with engine.connect() as conn:
        status = conn.execute(select(Session.show_polygons).where(Session.username == username)).scalar_one()
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


def get_line_width(username: str) -> int:
    with engine.connect() as conn:
        line_width = conn.execute(select(Session.line_width).where(Session.username == username)).scalar_one()
    return line_width


def get_line_opacity(username: str) -> float:
    with engine.connect() as conn:
        opacity = conn.execute(select(Session.line_opacity).where(Session.username == username)).scalar_one()
    return opacity

def get_fill_opacity(username: str) -> float:
    with engine.connect() as conn:
        opacity = conn.execute(select(Session.fill_opacity).where(Session.username == username)).scalar_one()
    return opacity


def get_zoom_value(username: str) -> float:
    with engine.connect() as conn:
        zoom_value = conn.execute(select(Session.zoom_value).where(Session.username == username)).scalar_one()
    return zoom_value


def get_wheel_zoom(username: str) -> bool:
    with engine.connect() as conn:
        wheel_zoom = conn.execute(select(Session.wheel_zoom).where(Session.username == username)).scalar_one()
    return wheel_zoom

def get_opened_settings(username: str) -> bool:
    with engine.connect() as conn:
        opened_settings = conn.execute(select(Session.opened_settings).where(Session.username == username)).scalar_one()
    return opened_settings

def update_opened_settings(username: str, opened_settings: bool):
    with engine.connect() as conn:
        with conn.begin():
            conn.execute(update(Session).values(opened_settings=opened_settings).where(Session.username == username))

def update_wheel_zoom(username: str, wheel_zoom: bool):
    with engine.connect() as conn:
        with conn.begin():
            conn.execute(update(Session).values(wheel_zoom=wheel_zoom).where(Session.username == username))


def update_zoom_value(username: str, zoom_value: int):
    with engine.connect() as conn:
        with conn.begin():
            conn.execute(update(Session).values(zoom_value=zoom_value).where(Session.username == username))


def update_fill_opacity(username: str, opacity: int):
    with engine.connect() as conn:
        with conn.begin():
            conn.execute(update(Session).values(fill_opacity=opacity).where(Session.username == username))


def update_line_opacity(username: str, opacity: int):
    with engine.connect() as conn:
        with conn.begin():
            conn.execute(update(Session).values(line_opacity=opacity).where(Session.username == username))


def update_line_width(username: str, line_width: int):
    with engine.connect() as conn:
        with conn.begin():
            conn.execute(update(Session).values(line_width=line_width).where(Session.username == username))


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
            

def update_show_polygons(username: str, show_polygons: bool):
    with engine.connect() as conn:
        with conn.begin():
            conn.execute(update(Session).values(show_polygons=show_polygons).where(Session.username == username))