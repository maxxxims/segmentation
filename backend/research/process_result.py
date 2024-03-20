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
from pathlib import Path
from tqdm import tqdm



class Config:
    PATH_TO_BORDERS = Path(r'C:\Users\maxxx\VSprojects\back\0\0\border')
    MAIN_FOLDER = Path(r'C:\Users\maxxx\VSprojects\back')    # parent folder with images
    IMGTAG2BORDER = {
    'ex0_300': PATH_TO_BORDERS / '0.png',
    'ex1_300': PATH_TO_BORDERS / '0.png',
    'ex2_300': PATH_TO_BORDERS / '4.png',
    'ex3_300': PATH_TO_BORDERS / '3.png',
    'ex4_300': PATH_TO_BORDERS / '5.png',
    'ex4_300': PATH_TO_BORDERS / '6.png',
    }
    RELATIVE_PATH_TO_GT = Path(r'02. Segmented\00. Original')
    N_PORES_DIAMETR = 7
    SAVE_FOLDER = Path('backend') / 'research' / 'images' / 'v2_10' # relative folder to save
MASK_VALUE = 0.5

class Ticker:
    i = 0
    @classmethod
    def plus(cls):
        cls.i += 1

def parse_folder(path_to_folder: str):
    """
        returm map file_name to folders names with atempts
    """
    tag2resultfile = defaultdict(list)
    result_files = os.listdir(path_to_folder)
    for result_file in result_files:
        if 'result' in result_file:    
            file_names = [el for el in os.listdir(os.path.join(path_to_folder, result_file)) if el.endswith('.png')]
            image_tag  = file_names[0].split('.')[0]
            tag2resultfile[image_tag].append(result_file)
    return tag2resultfile



def load_result_json(path_to_result_folder: Path):
    """
        load json file with result of annotation
    """
    file_name = path_to_result_folder / 'result.json'
    with open(file_name, 'r') as f:
        result = json.load(f)
    return result


def load_original_image(result: dict, MAIN_FOLDER: Path) -> Image:
    original_image_path = MAIN_FOLDER / result['folder_path'] / result['relative_image_path'] / result['image_name']
    original_image = Image(path_to_image=original_image_path)
    return original_image


def load_gt_image(result: dict, MAIN_FOLDER: Path, RELATIVE_PATH_TO_GT: Path):
    gt_image_path = MAIN_FOLDER / result['folder_path'] / RELATIVE_PATH_TO_GT / result['image_name']
    gt_image = Image(path_to_image=gt_image_path)
    return gt_image


def get_marker_container(result: dict):
    marker_class1 = MarkerByPoints2D(x_indexes=np.array(result['x_1_class'])+ result['width0'], 
                                    y_indexes=np.array(result['y_1_class'])+ result['height0'], value=1)
    marker_class0 = MarkerByPoints2D(x_indexes=np.array(result['x_0_class'])+ result['width0'], 
                                    y_indexes=np.array(result['y_0_class'])+ result['height0'], value=0)
    return MarkerContainer([marker_class1, marker_class0])

def get_img(data: dict):
    img = np.zeros(shape=(300, 300))
    img[data['y_1_class'], data['x_1_class']] = 1
    return img

def get_replaced_procentage(arr: np.ndarray, data: dict):
    assert len(data['y_1_class']) + len(data['y_0_class']) == 300 ** 2, 'ERROR!'
    pixels_1_class = len(data['y_1_class'])
    return np.sum(arr == MASK_VALUE) / pixels_1_class * 100


def get_changed_marker_container(result: dict, size: int):
    img = get_img(result)
    mask = filters_2d.Erosion(size=size).make_mask(img)
    new_arr = np.copy(img)
    new_arr[img != img - mask] = MASK_VALUE
    print(f'prcntg = {get_replaced_procentage(new_arr, result)}')
    y_1_class, x_1_class,  = np.where(new_arr == 1)
    y_0_class, x_0_class = np.where(new_arr == 0)

    marker_class1 = MarkerByPoints2D(x_indexes=np.array(x_1_class)+ result['width0'], 
                                    y_indexes=np.array(y_1_class)+ result['height0'], value=1)
    marker_class0 = MarkerByPoints2D(x_indexes=np.array(x_0_class)+ result['width0'], 
                                    y_indexes=np.array(y_0_class)+ result['height0'], value=0)
    return MarkerContainer([marker_class1, marker_class0])


def get_border_marker(result: dict, IMGTAG2BORDER: dict):
    border_img_path = IMGTAG2BORDER[result['image_tag']]
    border_marker = MarkerBorder2D(Image(path_to_image=border_img_path))
    return border_marker


def get_accuracy(result: dict):
    acc = result['accuracy']
    return acc


def draw_all_markers(original_image: Image, markers: MarkerContainer, border_marker: MarkerBorder2D):
    for m in markers:
        original_image.draw_marker(m, color=255 * m.value)
    original_image.draw_marker(border_marker, color=1)
    original_image.show()
    original_image.reset()
    #original_image.show()



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

def eval_segmentation(segmented, gt_image, markers, border_marker, N_PORES_DIAMETR):
    METRICS = [EPorosity, IoU_pores]
    METRICS_BORDER = [F1_binary, IoU_pores]
    res1 = Evaluator.evaluate(segmented, gt_image, markers, border_marker, *METRICS)
    res2 = EvaluatorBorder.evaluate(N_PORES_DIAMETR, segmented, gt_image, markers, border_marker, *METRICS_BORDER)
    for key, value in res2.items():
        res1[f'{key}_{N_PORES_DIAMETR}'] = value
    return res1


def save_result_to_csv(metrics: dict, operation_name: str, image_name: str, path_to_csv: Path):
    cols = ['operation_name', 'image_name', 'EPorosity', 'IoU_pores', 'F1_binary_7', 'IoU_pores_7']
    row = [operation_name, image_name, metrics['Porosity relative difference'], metrics['IoU_pores'],
            metrics['F1 binary_7'], metrics['IoU_pores_7']]
    new_data = pd.DataFrame([row], columns=cols)

    if path_to_csv.exists():
        df = pd.read_csv(path_to_csv)
        df = pd.concat([df, new_data])
    else:
        df = new_data
    df.to_csv(path_to_csv, index=False)


def process_one_attempt(path_to_result_folder: str, operation_name: str, image_name: str, cfg: Config): 
    result = load_result_json(path_to_result_folder)
    original_image = load_original_image(result, MAIN_FOLDER=cfg.MAIN_FOLDER)
    marker_container = get_marker_container(result)
    border_marker = get_border_marker(result, IMGTAG2BORDER=cfg.IMGTAG2BORDER)

    gt_image = load_gt_image(result, MAIN_FOLDER=cfg.MAIN_FOLDER, RELATIVE_PATH_TO_GT=cfg.RELATIVE_PATH_TO_GT)

    #draw_all_markers(original_image, marker_container, border_marker)
    #gt_image.show()

    segmented = segmentate_image(original_image, marker_container)
    #segmented.show()
    save_folder = cfg.SAVE_FOLDER / f'opetator_{operation_name}'
    save_folder.mkdir(exist_ok=True, parents=True)
    segmented.save(save_folder / f'{image_name}_{Ticker.i}.png')
    Ticker.plus()
    metrics = eval_segmentation(segmented, gt_image, marker_container, border_marker, cfg.N_PORES_DIAMETR)
    print(metrics)
    csv_save_folder = cfg.SAVE_FOLDER / 'result.csv'
    save_result_to_csv(metrics, operation_name, image_name, csv_save_folder)



def process_one_attempt_prcntg(path_to_result_folder: Path, operation_name: str, image_name: str, prcntg: float, cfg: Config): 
    cfg.SAVE_FOLDER = Path('backend') / 'research' / 'images' / f'v2_{prcntg}'
    df = pd.read_csv(path_to_result_folder.parent / 'prcntg2size.txt', sep=' ', header=None)
    df.columns = ['img_name', 'prcntg', 'size']
    size = df[(df['img_name'] == f'{image_name}.png') & (df['prcntg'] == prcntg)]['size'].values[0]

    result = load_result_json(path_to_result_folder)
    original_image = load_original_image(result, MAIN_FOLDER=cfg.MAIN_FOLDER)
    marker_container = get_changed_marker_container(result, size=size)
    border_marker = get_border_marker(result, IMGTAG2BORDER=cfg.IMGTAG2BORDER)

    gt_image = load_gt_image(result, MAIN_FOLDER=cfg.MAIN_FOLDER, RELATIVE_PATH_TO_GT=cfg.RELATIVE_PATH_TO_GT)

    #draw_all_markers(original_image, marker_container, border_marker)
    #gt_image.show()

    segmented = segmentate_image(original_image, marker_container)
    #segmented.show()
    save_folder = cfg.SAVE_FOLDER / f'opetator_{operation_name}'
    save_folder.mkdir(exist_ok=True, parents=True)
    segmented.save(save_folder / f'{image_name}_{Ticker.i}.png')
    Ticker.plus()
    metrics = eval_segmentation(segmented, gt_image, marker_container, border_marker, cfg.N_PORES_DIAMETR)
    print(metrics)
    csv_save_folder = cfg.SAVE_FOLDER / 'result.csv'
    save_result_to_csv(metrics, operation_name, image_name, csv_save_folder)


def main(path_to_folder: Path, operation_name: str, replaced_prcntg: float = 0):
    tag2resultfile = parse_folder(path_to_folder)
    for image_tag in tqdm(tag2resultfile.keys()):
        for result_folder in tag2resultfile[image_tag]:
            path_to_result_folder = path_to_folder / result_folder
            if replaced_prcntg == 0:
                process_one_attempt(path_to_result_folder, operation_name=operation_name, image_name=image_tag, cfg=Config())
            else:
                process_one_attempt_prcntg(path_to_result_folder, operation_name=operation_name, image_name=image_tag, prcntg=replaced_prcntg, cfg=Config())



if __name__ == '__main__':
    # parse_folder(r'C:\Users\maxxx\VSprojects\back\msa\outputA')
    # correct(r'C:\Users\maxxx\VSprojects\back\msa\outputA')
    main_folder = Path(r'C:\Users\maxxx\VSprojects\back\msa\corrected')
    main(main_folder / 'outputA', operation_name='A', replaced_prcntg=70)
    main(main_folder / 'outputC', operation_name='C', replaced_prcntg=70)    
    main(main_folder / 'my_B', operation_name='B', replaced_prcntg=70)