from ..image import Image, MarkerByPoints2D, MarkerBorder2D, MarkerContainer
from ..filters import filters_2dim as filters_2d
from ..metrics import Evaluator, Accuracy, F1_binary, EPorosity, IoU_pores, EvaluatorBorder
from ..segmentation import Segmentation
import os
import json
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from collections import defaultdict


MAIN_FOLDER = r'C:\Users\maxxx\VSprojects\back'
RELATIVE_PATH_TO_GT = r'02. Segmented\00. Original'
PATH_TO_BORDERS = r'C:\Users\maxxx\VSprojects\back\0\0\border'
EXP_CSV = os.path.join('backend', 'research', 'experiments.csv') # os.getcwd(), 
N_PORES_DIAMETR = 3
IMGTAG2BORDER = {
    'ex0_300': os.path.join(PATH_TO_BORDERS, '0.png'),
    'ex1_300': os.path.join(PATH_TO_BORDERS, '0.png'),
    'ex2_300': os.path.join(PATH_TO_BORDERS, '4.png'),
    'ex3_300': os.path.join(PATH_TO_BORDERS, '3.png'),
    'ex4_300': os.path.join(PATH_TO_BORDERS, '5.png'),
    'ex4_300': os.path.join(PATH_TO_BORDERS, '6.png'),
}

COL2COL = {'Operator': 'Operator', 'Image': 'Image', 'Porosity relative difference': 'eps',
            'IoU_pores': 'IoU', 'F1 binary_3': 'F1_3', 'IoU_pores_3': 'IoU_3'}

OPERATORS = ['A', 'B', 'C', 'D']


__PATH_TO_3_GT = r'C:\Users\maxxx\VSprojects\back\segmentation\data\input\ex3_300_annotated.npy'

if not os.path.isfile(EXP_CSV):
    df = pd.DataFrame(columns=COL2COL.values())
    df.to_csv(EXP_CSV, index=False)


def parse_folder(path_to_folder: str):
    tag2resultfile = defaultdict(list)
    result_files = os.listdir(path_to_folder)
    for result_file in result_files:
        if 'result' in result_file:    
            file_names = [el for el in os.listdir(os.path.join(path_to_folder, result_file)) if el.endswith('.png')]
            image_tag  = file_names[0].split('.')[0]
            tag2resultfile[image_tag].append(result_file)
    return tag2resultfile


def calc_ss_ms():
    ...



def process_one_result_file(path_to_result_folder: str, **kwargs: dict):
    file_name = os.path.join(path_to_result_folder, 'result.json')
    with open(file_name, 'r') as f:
        result = json.load(f)
    original_image_path = os.path.join(MAIN_FOLDER, result['folder_path'],
                                        result['relative_image_path'], result['image_name'])
    gt_image_path = os.path.join(MAIN_FOLDER, result['folder_path'],
                                 RELATIVE_PATH_TO_GT, result['image_name'])
    border_img_path = IMGTAG2BORDER[result['image_tag']]
    original_image = Image(path_to_image=original_image_path)
    gt_image = Image(path_to_image=gt_image_path)


    acc = result['accuracy']
    if 'ex3_300' in kwargs.get('image_name', ' '):
        gt_data = np.load(__PATH_TO_3_GT)
        gt_data[gt_data > 0] = 1
        orig_data = np.zeros_like(gt_data)
        orig_data[result['y_0_class'], result['x_0_class']] = 1
        acc = np.sum(orig_data == gt_data) / ( orig_data.shape[0] * orig_data.shape[1])
        # Image(data=orig_data).show()
        print(f'acc = {acc}')

        marker_class0 = MarkerByPoints2D(x_indexes=np.array(result['x_1_class'])+ result['width0'], 
                                        y_indexes=np.array(result['y_1_class'])+ result['height0'], value=0)
        marker_class1 = MarkerByPoints2D(x_indexes=np.array(result['x_0_class'])+ result['width0'], 
                                        y_indexes=np.array(result['y_0_class'])+ result['height0'], value=1)
    
    
    else:
            
        marker_class1 = MarkerByPoints2D(x_indexes=np.array(result['x_1_class'])+ result['width0'], 
                                        y_indexes=np.array(result['y_1_class'])+ result['height0'], value=1)
        marker_class0 = MarkerByPoints2D(x_indexes=np.array(result['x_0_class'])+ result['width0'], 
                                        y_indexes=np.array(result['y_0_class'])+ result['height0'], value=0)
    

    border_marker = MarkerBorder2D(Image(path_to_image=border_img_path))
    # for m in [marker_class1, marker_class0]:
    #     original_image.draw_marker(m, color=m.value * 255)  
    # original_image.draw_marker(border_marker, color=0)  
    # original_image.show()
    # exit(0)
    #print(result.keys())
    


    return original_image, gt_image, \
            MarkerContainer([marker_class1, marker_class0]), border_marker, acc
    
    
def segmentate_image(original_image, markers):
    filters = [
                filters_2d.MedianFilter(size=5),   filters_2d.GaussianFilter(15),
                filters_2d.VarianceFilter(size=6), filters_2d.HighPassFilter(k=9), filters_2d.BaseFilter2D(), 
                filters_2d.Erosion(size=3), filters_2d.Dilation(size=3),
                filters_2d.Closing(size=3), filters_2d.Opening(size=3)
              ]
    
    for ii in [2, 4]:
        scalled_filters =[
                    filters_2d.MedianFilter(size=5, scale=ii),   filters_2d.GaussianFilter(15, scale=ii),
                    filters_2d.BaseFilter2D(scale=ii), 
                    filters_2d.Erosion(size=3, scale=ii), filters_2d.Dilation(size=3, scale=ii),
                    filters_2d.Closing(size=3, scale=ii), filters_2d.Opening(size=3, scale=ii)
                  ]
        filters += scalled_filters
    sgm = Segmentation(model=RandomForestClassifier(n_jobs=-1, random_state=42), filters=filters)
    result = sgm.fit_and_predict(original_image, markers)
    return result


def eval_segmentation(segmented, gt_image, markers, border_marker):
    METRICS = [EPorosity, IoU_pores]
    METRICS_BORDER = [F1_binary, IoU_pores]
    res1 = Evaluator.evaluate(segmented, gt_image, markers, border_marker, *METRICS)
    res2 = EvaluatorBorder.evaluate(N_PORES_DIAMETR, segmented, gt_image, markers, border_marker, *METRICS_BORDER)
    for key, value in res2.items():
        res1[f'{key}_{N_PORES_DIAMETR}'] = value

    return res1


def save_result_to_csv(metrics: dict, accuracy, operation_name: str, image_name: str, path_to_csv: Path):
    df = pd.read_csv(EXP_CSV)
    
    row = [operation_name, image_name, metrics['Porosity relative difference'], metrics['IoU_pores'],
            metrics['F1 binary_3'], metrics['IoU_pores_3'], accuracy]
    new_data = pd.DataFrame([row], columns=df.columns)
    if len(df) != 0:
        df = pd.concat([df, new_data])
    else:
        df = new_data
    df.to_csv(EXP_CSV, index=False)


class Ticker:
    i = 0
    @classmethod
    def plus(cls):
        cls.i += 1


def process_one_attempt(path_to_result_folder: str, operation_name: str, image_name: str):
    original_image, gt_image, markers, border_marker, accuracy = process_one_result_file(path_to_result_folder, image_name=image_name)
    segmented = segmentate_image(original_image, markers)
    segmented.save(os.path.join('backend', 'research', f'{image_name}_{Ticker.i}.png'))
    Ticker.plus()
    metrics = eval_segmentation(segmented, gt_image, markers, border_marker)
    print(path_to_result_folder, metrics)
    # metrics = {'Porosity relative difference': 8.935637160986325,
    #             'IoU_pores': 0.8918857032130612, 'F1 binary_3': 0.6942290930483932,
    #               'IoU_pores_3': 0.27741186404897616}
    # print(metrics)
    save_result_to_csv(metrics, accuracy, operation_name, image_name)


def main(path_to_folder: str, operation_name: str):
    tag2resultfile = parse_folder(path_to_folder)
    for image_tag in tag2resultfile.keys():
        for result_folder in tag2resultfile[image_tag]:
            path_to_result_folder = os.path.join(path_to_folder, result_folder)
            process_one_attempt(path_to_result_folder, operation_name=operation_name, image_name=image_tag)


def correct(path_to_folder):
    acc_arr = []
    tag2resultfile = parse_folder(path_to_folder)
    for image_tag in tag2resultfile.keys():
        print(image_tag)
        if 'ex3_300' in image_tag:
            for result_folder in tag2resultfile[image_tag]:
                path_to_result_folder = os.path.join(path_to_folder, result_folder)
                original_image, gt_image, markers, border_marker, accuracy = process_one_result_file(path_to_result_folder)
                acc_arr.append(accuracy)
                print(f'folder = {result_folder}')
    df = pd.read_csv(EXP_CSV)
    df['Annotation_accuracy'] = np.array(acc_arr)
    print(df.head())
    df.to_csv(EXP_CSV, index=False)
    

if __name__ == '__main__':
    # parse_folder(r'C:\Users\maxxx\VSprojects\back\msa\outputA')
    # correct(r'C:\Users\maxxx\VSprojects\back\msa\outputA')
    main(r'C:\Users\maxxx\VSprojects\back\msa\outputC', operation_name='C') 