from pathlib import Path
import numpy as np
import dash


def save_image(username: str, img: np.ndarray):
    if not hasattr(dash.get_app(), 'image_storage'):
        dash.get_app().__setattr__('image_storage', {})
    dash.get_app().image_storage[username] = img


def get_image(username: str) -> np.ndarray:
    if not hasattr(dash.get_app(), 'image_storage'):
        return None
    return dash.get_app().image_storage[username]

# def save_image(username: str, img: np.ndarray):
#     path_to_save = Path(f'GUI/storage/{username}')
#     path_to_save.mkdir(parents=True, exist_ok=True)
#     np.save(path_to_save / 'image.npy', img)


# def get_image(username: str) -> np.ndarray:
#     return np.load(Path(f'GUI/storage/{username}') / 'image.npy')