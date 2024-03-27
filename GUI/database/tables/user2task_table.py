from pathlib import Path
from ..db import engine
from ..models import Task, User2Task, Session, User
from sqlalchemy import select, insert, update, delete, and_, desc, asc, func, case
from uuid import uuid4, UUID
from sqlalchemy.orm import joinedload


def add_task(username: str, task_id: int, attempt_number: int):
    with engine.connect() as conn:
        with conn.begin():
            conn.execute(insert(User2Task).values(username=username, task_id=task_id, attempt_number=attempt_number))


def get_available_tasks(username: str) -> list:
    with engine.begin() as conn:
        result = conn.execute(select(User2Task, Task).join(Task, Task.id == User2Task.task_id).where(and_(User2Task.username == username,
                                                           User2Task.finished == False)))
    return result.all()


def get_users_tasks_info():
    with engine.begin() as conn:
        count_finished = func.sum(case((User2Task.finished == True, 1),
                                       else_=0))#.label('count_finished'))
        all_tasks = func.count(User2Task.uuid)#.label('all_tasks')
        
        query = select(User2Task.username, User.name, Session.last_activity, count_finished, all_tasks)
        query = query.group_by(
                       User2Task.username).join(
                       Session, User2Task.username == Session.username
                   ).join(
                       User, User.username == User2Task.username
                   )
        result = conn.execute(query).all()
    return result
        


def get_current_task_uuid(username: str) -> UUID:
    with engine.begin() as conn:
        uuid = conn.execute(select(User2Task.uuid).where(and_(User2Task.username == username,
                                                                    User2Task.is_choosen == True))).first()
    if uuid is None:
        return None
    else:
        return uuid.uuid


def get_current_task_attempt_number(username: str) -> int:
    with engine.begin() as conn:
        attempt_number = conn.execute(select(User2Task.attempt_number).where(and_(User2Task.username == username,
                                                                    User2Task.is_choosen == True))).first()
    if attempt_number is None:
        return None
    else:
        return attempt_number.attempt_number


def get_all_tasks(username: str) -> list:
    with engine.begin() as conn:
        result = conn.execute(select(User2Task, Task).join(
            Task, Task.id == User2Task.task_id).where(User2Task.username == username).order_by(
                Task.image_name.asc(), User2Task.attempt_number.asc()
            ))
    return result.all()


def get_task_by_id(task_id: int) -> Task:
    with engine.begin() as conn:
        result = conn.execute(select(Task).where(Task.id == task_id))
    return result.first()


def get_task_by_uuid(uuid: UUID) -> Task:
    with engine.begin() as conn:
        result = conn.execute(select(User2Task, Task).join(Task, Task.id == User2Task.task_id).where(User2Task.uuid == uuid))
    return result.first()


def update_finished(username: str, uuid: UUID, finished: bool):
    with engine.connect() as conn:
        with conn.begin():
            conn.execute(update(User2Task).values(finished=finished).where(and_(User2Task.username == username, User2Task.uuid == uuid)))
            
            
def update_save_folder(username: str, uuid: UUID, save_folder: str):
    if isinstance(save_folder, Path):
        save_folder = str(save_folder)
    with engine.connect() as conn:
        with conn.begin():
            conn.execute(update(User2Task).values(save_folder=save_folder).where(and_(User2Task.username == username, User2Task.uuid == uuid)))
            
            
def update_choosen_task(uuid: UUID, is_choosen: bool):
    with engine.connect() as conn:
        with conn.begin():
            conn.execute(update(User2Task).where(User2Task.uuid == uuid).values(is_choosen=is_choosen))
            
            
def update_metric(uuid: UUID, metric: float):
    with engine.connect() as conn:
        with conn.begin():
            conn.execute(update(User2Task).values(metric=metric).where(User2Task.uuid == uuid))