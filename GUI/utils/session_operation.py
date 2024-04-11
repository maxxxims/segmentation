from uuid import UUID
from ..database import session_table, user2task_table, figure_table, image_table
import numpy as np


def set_gt_image_info(json_data: dict, username: str):
    annotatated_path = json_data['annotatated_path']
    gt_image = np.load(annotatated_path)
    class_0 = int(np.sum(gt_image == 0))
    class_1 = int(np.sum(gt_image > 0))
    figure_table.set_pixels_numbers(username, pixels_class_1=class_1, pixels_class_0=class_0)


def __clear_task(curent_task_uuid: UUID, username: str):
    user2task_table.update_choosen_task(uuid=curent_task_uuid, is_choosen=False)
    figure_table.delete_last_figure(username=username)
    figure_table.delete_marker_class_1(username=username)
    session_table.update_loaded_image(username=username, loaded_image=False)
    session_table.update_start_annotation(username=username, start_annotation=False)


def finish_task(username: str):
    """_summary_
    Clear data after save annotation
    
    Args:
        username (str): _description_
    """
    curent_task_uuid = user2task_table.get_current_task_uuid(username=username)    
    user2task_table.update_finished(username=username, uuid=curent_task_uuid, finished=True)
    __clear_task(curent_task_uuid, username)
    
    
def update_current_task(username: str, task_uuid: UUID, img: list, json_data: dict):
    """When user choose new task update current task, save image, json_data and update loaded image status

    Args:
        username (str): _description_
        task_id (UUID): _description_
    """
    previous_task_uuid = user2task_table.get_current_task_uuid(username=username)
    if previous_task_uuid is not None:
        __clear_task(previous_task_uuid, username)
        # print('try to finish task')
        # print(f'current uuid = {previous_task_uuid}, new_uuid = {task_uuid}')
        user2task_table.update_choosen_task(uuid=previous_task_uuid, is_choosen=False)
        # print('finish task')
    
    # print('task finished')
    user2task_table.update_choosen_task(uuid=task_uuid, is_choosen=True)
    # print('task finished 2')
    image_table.save_image(username, img)
    set_gt_image_info(json_data, username=username)
    figure_table.save_json_data(username=username, json_data=json_data)
    session_table.update_loaded_image(username=username, loaded_image=True)