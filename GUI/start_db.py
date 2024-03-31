from .utils import get_users, add_tasks_to_users, register_user, make_tasks_from_folder, register_users_from_csv, register_admin, start_sessions
from pathlib import Path
from .database.db import init_db


if __name__ == '__main__':
    init_db()
    register_admin()
    register_users_from_csv('users.csv')
    start_sessions()
    make_tasks_from_folder(path_to_folder=Path('data'), path_to_input_folder=Path('data/input'))
    add_tasks_to_users(attempts_per_user=3)