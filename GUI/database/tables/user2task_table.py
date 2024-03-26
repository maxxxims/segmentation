from ..db import engine
from ..models import Task, User2Task
from sqlalchemy import select, insert, update, delete, and_, desc, asc
from uuid import uuid4, UUID
from sqlalchemy.orm import joinedload


def add_task(username: str, task_id: int):
    with engine.connect() as conn:
        with conn.begin():
            conn.execute(insert(User2Task).values(username=username, task_id=task_id))


def get_available_tasks(username: str) -> list:
    with engine.begin() as conn:
        result = conn.execute(select(User2Task, Task).join(Task, Task.id == User2Task.task_id).where(and_(User2Task.username == username,
                                                           User2Task.finished == False)))
    return result.all()


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