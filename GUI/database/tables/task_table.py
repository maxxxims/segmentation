from ..db import engine
from ..models import Task
from sqlalchemy import select, insert, update, delete, and_, desc
from uuid import uuid4, UUID
from sqlalchemy.orm import joinedload


def add_task(image_name: str, path_to_json: str, path_to_image: str, path_to_annotated_image: str):
    with engine.connect() as conn:
        with conn.begin():
            conn.execute(insert(Task).values(image_name=image_name, path_to_annotated_image=path_to_annotated_image,
                                             path_to_json=path_to_json, path_to_image=path_to_image))


def get_tasks() -> list:
    with engine.begin() as conn:
        result = conn.execute(select(Task))
    return result.all()


def get_task_by_id(task_id: int) -> Task:
    with engine.begin() as conn:
        result = conn.execute(select(Task).where(Task.id == task_id))
    return result.first()