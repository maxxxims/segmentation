from pathlib import Path
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image as IMG
from svg.path import parse_path, path
import os
import json
from ..image import Image
from ..metrics import Evaluator, Accuracy


N_POINTS = int(1e3)
# ANNOTATION_COLOR = (0, 255, 0, 0)
# ANNOTATION_COLOR_BG = (150, 10, 0, 0)

MASK_VALUE = 255

MASK_VALUE_CLASS_1 = 255
MASK_VALUE_CLASS_0 = 128


def parse_path_to_save(path_to_save: Path, file_name: str) -> Path:
    """
        path_to_save = os.path.join('data', 'output')
        file_name = name of file
        return:
            path to result_ folder,
            path to result file

    """
    file_names = [el for el in os.listdir(path_to_save) if '.' not in el and 'result' in el]
    if len(file_names) == 0:
        dir =  "result1"
    else:
        numbers = [int(el.split('result')[-1]) for el in file_names]
        numbers.sort()
        dir =  f'result{numbers[-1] + 1}'
    path_to_result_folder = path_to_save / dir
    path_to_result_folder.mkdir(parents=True, exist_ok=True)
    return path_to_result_folder

"""
def OLD_save_annotation(img: np.ndarray, data: dict,  data_json: dict, path_to_save: Path,
                    folder_name: str, selected_class: int = 1,) -> tuple:
    
    data_pathes = []
    for el in data:
        if el["type"] == "path":
            data_pathes.append(el)

    stencil = draw_pathes(img, data_pathes)
    if selected_class == 1:
        select = stencil == MASK_VALUE
        select_bg = stencil != MASK_VALUE

    else:
        select = stencil != MASK_VALUE
        select_bg = stencil == MASK_VALUE

    #path_to_result_folder = parse_path_to_save(path_to_save, file_name)
    path_to_result_folder = path_to_save / folder_name
    path_to_result_folder.mkdir(parents=True, exist_ok=True)
    png_save_path = path_to_result_folder / f'{data_json["image_tag"]}.png'
    #print(png_save_path)

    # save png
    annotated_img = np.zeros((img.shape[0], img.shape[1]))
    annotated_img[select] = 255
    plt.imsave(png_save_path, annotated_img, cmap='gray')

    # save json
    #json_save_path = png_save_path.replace('.png', '.json')
    json_save_path = path_to_result_folder / 'result.json'
    
    y_1_class, x_1_class = np.where(select)
    y_0_class, x_0_class = np.where(select_bg)
    shape0, shape1 = stencil.shape[0], stencil.shape[1]

    data_for_save = {
        'shapes': data,
        "y_1_class": y_1_class.tolist(),
        "x_1_class": x_1_class.tolist(),
        "y_0_class": y_0_class.tolist(),
        "x_0_class": x_0_class.tolist(),
        "shape0": shape0,
        "shape1": shape1
    }

    for key, value in data_for_save.items():
        data_json[key] = value

    with open(json_save_path, 'w') as f:
        json.dump(data_json, f)

    return path_to_result_folder, data_json
"""
def save_annotation(annotated_image: np.ndarray, data: dict,  data_json: dict, path_to_save: Path,
                    folder_name: str) -> tuple:
    path_to_result_folder = path_to_save / folder_name
    path_to_result_folder.mkdir(parents=True, exist_ok=True)
    png_save_path = path_to_result_folder / f'{data_json["image_tag"]}.png'

    # save png
    plt.imsave(png_save_path, annotated_image, cmap='gray')

    # save json
    json_save_path = path_to_result_folder / 'result.json'

    
    y_1_class, x_1_class = np.where(annotated_image  == 255)
    y_0_class, x_0_class = np.where(annotated_image == 128)
    
    shape0, shape1 = annotated_image.shape[0], annotated_image.shape[1]

    data_for_save = {
        'shapes': data,
        "y_1_class": y_1_class.tolist(),
        "x_1_class": x_1_class.tolist(),
        "y_0_class": y_0_class.tolist(),
        "x_0_class": x_0_class.tolist(),
        "shape0": shape0,
        "shape1": shape1
    }

    for key, value in data_for_save.items():
        data_json[key] = value

    with open(json_save_path, 'w') as f:
        json.dump(data_json, f)

    return path_to_result_folder, data_json


def draw_pathes(_img: np.ndarray, data: list[dict]):
    """
        fill polygons with MASK_VALUE
    """
    img = np.copy(_img)
    n_polygons = len(data)
    pathes_arr = [parse_path(data[j]["path"]) for j in range(n_polygons)]

    contour = [[] for _ in range(n_polygons)]

    for i in range(N_POINTS):
        for j in range(n_polygons):
            point = pathes_arr[j].point(i / N_POINTS)
            x, y = round(np.real(point)), round(np.imag(point))
            contour[j].append(np.array([[x, y]]))

    contour = np.array(contour)

    stencil = np.zeros(img.shape[:2], dtype=np.uint8)
    # cv2.fillPoly(stencil, pts=contour, color=MASK_VALUE)
    for cnt in contour:
        cv2.fillPoly(stencil, pts=[cnt], color=MASK_VALUE)
        
    return stencil



def OLD_check_annotation(data: dict, selected_color: int, save_acc: bool = False,
                      path_to_save: bool = False, n_segments: int = -1):
    """
    :param data: json file with annotation to download file
    :param annotated_json_file_name: name of annotated file
    """
    selected_color = int(selected_color)
    ground_truth_path = os.path.join('data',   'input',  f'{data["image_tag"]}_annotated.npy')
    original_img_path = os.path.join('data',   'input',  f'{data["image_tag"]}.npy')

    # if original_img_path not in os.listdir(os.path.join('data', 'input')):
    #     raise Exception(f'Cannot find ground_truth file with path: \n{original_img_path}')
    
    #open cutted GT annotated and original image
    ground_truth_img = Image(data=np.load(ground_truth_path))
    original_img     = Image(data=np.load(original_img_path))
    print(f'{ground_truth_img.data.shape}, {original_img.data.shape}')

    if selected_color == 1:
        original_img.data[data['y_1_class'], data['x_1_class']] = 1
        original_img.data[data['y_0_class'], data['x_0_class']] = 0

    else:
        original_img.data[data['y_1_class'], data['x_1_class']] = 0
        original_img.data[data['y_0_class'], data['x_0_class']] = 1

    ground_truth_img.data[ground_truth_img.data > 0] = 1
 
    # markers_class_1 = MarkerByPoints2D(x_indexes=data['x_1_class'], y_indexes=data['y_1_class'])
    # markers_class_0 = MarkerByPoints2D(x_indexes=data['x_0_class'], y_indexes=data['y_0_class'])

    diffrence = np.zeros((ground_truth_img.data.shape[0], ground_truth_img.data.shape[1]), dtype=np.uint8)
    # print(diffrence.shape)
    diffrence[original_img.data != ground_truth_img.data] = 255

    acc = Evaluator.evaluate(ground_truth_img, original_img, [], None, Accuracy)

    if save_acc and path_to_save:
        data['accuracy']   = acc['Accuracy']
        data['n_segments'] = n_segments
        with open(os.path.join(path_to_save, 'result.json'), 'w') as f:
            json.dump(data, f, indent=4)

    #return acc, diffrence  
    return acc['Accuracy'], original_img



# def check_annotation(data: dict, _annotated_image: np.ndarray):
#     """ WORK ONLY TO FULL ANNOTATED IMAGE!!!
#     :param data: json file with annotation to download file
#     :param annotated_image: annotated image
#     """
#     ground_truth_path = Path(data["annotatated_path"])
#     ground_truth_img = Image(data=np.load(ground_truth_path))
#     ground_truth_img.data[ground_truth_img.data > 0] = 1
    
#     annotated_image = np.zeros_like(_annotated_image)
    
    
#     annotated_image[annotated_image > 0] = 1
#     acc = Evaluator.evaluate(ground_truth_img, Image(data=annotated_image), [], None, Accuracy)
#     diffrence = np.zeros_like(annotated_image)
#     diffrence[annotated_image != ground_truth_img.data] = 1
#     # plt.imsave('diffrence.png', diffrence, cmap='gray')
#     # plt.imsave('annotated.png', annotated_image, cmap='gray')
#     # plt.imsave('ground_truth.png', ground_truth_img.data, cmap='gray')
#     # print(f'MY CALCT ACC = {np.sum(diffrence == 0) / diffrence.size}; size = {diffrence.size}')
    
#     return acc['Accuracy'], ground_truth_img


def check_annotation(data: dict, annotated_image: np.ndarray):
    ground_truth_path = Path(data["annotatated_path"])
    ground_truth_img = Image(data=np.load(ground_truth_path))
    ground_truth_img.data[ground_truth_img.data > 0] = 1
    
    annotated_area = annotated_image != 0
    
    gt_data = ground_truth_img.data[annotated_area]
    annotated_data = annotated_image[annotated_area]
    assert np.sum(annotated_data == 0) == 0, 'Something wrong with annotating process!!!'
    annotated_data[annotated_data == 255] = 1
    annotated_data[annotated_data == 128] = 0
    
    acc = np.sum(gt_data == annotated_data) / gt_data.size
    return acc