from ..db import redis
import json

def __redis_get(key: str):
    value = redis.get(key)
    if value is None:
        return None
    return json.loads(value)




def save_last_figure(username: str, figure: dict):
    value = json.dumps(figure)
    redis.set(f'figure_{username}', value)

def get_last_figure(username: str) -> dict:
    return __redis_get(f'figure_{username}')

def delete_last_figure(username: str):
    redis.delete(f'figure_{username}')


def save_marker_class_1(username: str, marker_class_1: list):
    redis.set(f'marker_class_1_{username}', json.dumps(marker_class_1))

def get_marker_class_1(username: str) -> list:
    return __redis_get(f'marker_class_1_{username}')

def delete_marker_class_1(username: str):
    redis.delete(f'marker_class_1_{username}')


def save_json_data(username: str, json_data: dict):
    redis.set(f'json_data_{username}', json.dumps(json_data))
    

def get_json_data(username: str) -> dict:
    return __redis_get(f'json_data_{username}')