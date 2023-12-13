from ..image import Image, MarkerBorder2D, MarkerByPoints2D, MarkerContainer
from ..segmentation import Segmentation
from ..metrics import Evaluator, Accuracy
from backend.filters import  filters_2dim as filters_2d
import json
import os
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier



BORDER_PATH = r'C:\Users\maxxx\VSprojects\back\0\0\border\border00001.png'
IMG2BORDER = {}
PATH_TO_OUTPUT = 'data/output'


MAIN_FOLDER = r'C:\Users\maxxx\VSprojects\back'
RELATIVE_GT_PATH = r'02. Segmented\00. Original'


def correct_indexes(indx_arr, delta):
    return np.array(indx_arr) + delta


def crop_area(max_size: tuple, data: dict):
    x_indexes_1_new, y_indexes_1_new, x_indexes_0_new, y_indexes_0_new = [], [], [], []
    max_x, max_y = max_size
    for i in range(len(data['x_0_class'])):
        if data['x_0_class'][i] < max_x and data['y_0_class'][i] < max_y:
            x_indexes_0_new.append(data['x_0_class'][i])
            y_indexes_0_new.append(data['y_0_class'][i])
    
    for i in range(len(data['x_1_class'])):
        if data['x_1_class'][i] < max_x and data['y_1_class'][i] < max_y:
            x_indexes_1_new.append(data['x_1_class'][i])
            y_indexes_1_new.append(data['y_1_class'][i])
    data['x_0_class'] = x_indexes_0_new
    data['y_0_class'] = y_indexes_0_new
    data['x_1_class'] = x_indexes_1_new
    data['y_1_class'] = y_indexes_1_new


def parse_json(file_path: str):
    path_to_json = os.path.join(PATH_TO_OUTPUT, file_path, 'result.json')
    with open(path_to_json, 'r') as file:
        data = json.load(file)

    # crop_area((50, 50), data)

    x_indexes_1 = correct_indexes(data['x_1_class'], data['width0'])
    y_indexes_1 = correct_indexes(data['y_1_class'], data['height0'])
    x_indexes_0 = correct_indexes(data['x_0_class'], data['width0'])
    y_indexes_0 = correct_indexes(data['y_0_class'], data['height0'])

    return data, x_indexes_1, y_indexes_1, x_indexes_0, y_indexes_0

def segmentate_image_from_result_file(file_path: str):
    
    data, x_indexes_1, y_indexes_1, x_indexes_0, y_indexes_0 = parse_json(file_path)

    path_to_orig_img = os.path.join(MAIN_FOLDER, data['folder_path'], data['relative_image_path'], data['image_name'])
    path_to_gt = os.path.join(MAIN_FOLDER, data['folder_path'], RELATIVE_GT_PATH, data['image_name'])
    

    img_orig = Image(path_to_orig_img)
    border_marker = MarkerBorder2D(image_border=Image(BORDER_PATH))
    

    annotation_marker_1 = MarkerByPoints2D(x_indexes=x_indexes_1,
                                           y_indexes=y_indexes_1, value=1)
    
    annotation_marker_0 = MarkerByPoints2D(x_indexes=x_indexes_0,
                                           y_indexes=y_indexes_0, value=0)

    markers = MarkerContainer([annotation_marker_1, annotation_marker_0])

    img_orig2 = Image(path_to_orig_img)

    # img_orig.draw_marker(border_marker, color=0)
    # img_orig.draw_marker(annotation_marker_1, color=255)
    # img_orig.draw_marker(annotation_marker_0, color=0)
    # img_orig.show_images(1, 2,img_orig, img_orig2)#, p1=(1750, 800), p2=(1750+300, 800 + 300))
    # return 0


    filters = [
            filters_2d.MedianFilter(size=5),   filters_2d.GaussianFilter(15),  filters_2d.LaplacianDifference(),
            filters_2d.VarianceFilter(size=3), filters_2d.HighPassFilter(k=9), filters_2d.BaseFilter2D(), 
          ]
    sgm = Segmentation(RandomForestClassifier(n_jobs=-1), filters=filters, informing=False)

    result = sgm.fit_and_predict(img_orig, markers)
    result.show(title='Segmentated Image')


    ground_truth = Image(path_to_image=path_to_gt, dim=2)
    res = Evaluator.evaluate(result, ground_truth, markers, border_marker, Accuracy)
    print(res)
    
    # print(data.keys())
    # print(data['original_image_name'], data['image_path'])
    ...


segmentate_image_from_result_file('result1')