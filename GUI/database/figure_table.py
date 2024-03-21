from .db import redis
import json

def __redis_get(key: str):
    value = redis.get(key)
    if value is None:
        return None
    return json.loads(value)


def save_last_figure(username: str, figure: dict):
    value = json.dumps(figure)
    #value = value.replace('true', 'True')
    redis.set(f'figure_{username}', value)


def get_last_figure(username: str) -> dict:
    #return json.loads(redis.get(f'figure_{username}'))
    return __redis_get(f'figure_{username}')

def save_marker_class_1(username: str, marker_class_1: list):
    redis.set(f'marker_class_1_{username}', json.dumps(marker_class_1))

def get_marker_class_1(username: str) -> list:
    #return json.loads(redis.get(f'marker_class_1_{username}'))
    return __redis_get(f'marker_class_1_{username}')