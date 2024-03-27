import os
from pathlib import Path
from ..database import user_table, session_table, task_table, user2task_table
import json

def register_user(username: str, passwrod: str, name = None):
    """
    Register new user
    """
    user_table.add_user(username=username, password=passwrod, name=name)
    session_table.create_session(username=username)
    
    

def make_tasks_from_folder(path_to_folder: Path, path_to_input_folder: Path):
    for f_name in os.listdir(path_to_folder):
        if f_name.endswith('.json'):
            with open(path_to_folder / f_name, 'r') as file:
                config_file = json.load(file)
            image_name = config_file['image_tag']
            path_to_json = str(path_to_folder / f_name)
            path_to_image = str(path_to_input_folder / f'{image_name}.npy')
            path_to_annotated_image = str(path_to_input_folder / f'{image_name}_annotated.npy')
            task_table.add_task(image_name=image_name, path_to_json=path_to_json,
                        path_to_image=path_to_image,
                        path_to_annotated_image=path_to_annotated_image)
            
            
def add_tasks_to_users(attempts_per_user: int = 1):
    users = user_table.get_users()
    tasks = task_table.get_tasks()
    for user in users:
        for task in tasks:
            for attempt_number in range(attempts_per_user):
                user2task_table.add_task(username=user.username, task_id=task.id, attempt_number=attempt_number+1)