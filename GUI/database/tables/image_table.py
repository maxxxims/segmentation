from pathlib import Path
import numpy as np
import dash
from .user2task_table import get_current_task_uuid, get_task_by_uuid
from .session_table import is_loaded_image

def save_image(username: str, img: np.ndarray):
    if not hasattr(dash.get_app(), 'image_storage'):
        dash.get_app().__setattr__('image_storage', {})
    dash.get_app().image_storage[username] = img


def _get_image(username: str) -> np.ndarray:
    if not hasattr(dash.get_app(), 'image_storage'):
        return None
    return dash.get_app().image_storage.get(username, None)


def get_image(username: str) -> np.ndarray:
    img = _get_image(username)
    if img is None:
        has_img = is_loaded_image(username)
        task_uuid = get_current_task_uuid(username)
        if task_uuid is not None and has_img:
            task = get_task_by_uuid(task_uuid)
            path_to_img = Path(str(task.path_to_image).replace('\\', '/'))
            _img = np.load(path_to_img)
            img = np.zeros((*_img.shape, 3), dtype=np.uint8)
            for i in range(3):
                img[:, :, i] = _img
            save_image(username, img)
    return img
# def save_image(username: str, img: np.ndarray):
#     path_to_save = Path(f'GUI/storage/{username}')
#     path_to_save.mkdir(parents=True, exist_ok=True)
#     np.save(path_to_save / 'image.npy', img)


# def get_image(username: str) -> np.ndarray:
#     return np.load(Path(f'GUI/storage/{username}') / 'image.npy')