import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from svg.path import parse_path, path
from .save_annotation import draw_pathes as draw_pathes_another, MASK_VALUE, MASK_VALUE_CLASS_1, MASK_VALUE_CLASS_0
import base64
import io


N_POINTS = int(1e3)
ANNOTATION_COLOR = (0, 255, 0, 0)

ANNOTATION_COLOR_BG = (150, 10, 0, 0)


ANNOTATION_COLOR_CLASS_1 = (0, 255, 0)
ANNOTATION_COLOR_CLASS_0 = (255, 0, 0)



def normalize_img(img: np.ndarray):
    new_arr = np.copy(img)
    print(f'SHAPE = {img.shape}')
    for i in range(3):
        new_arr[:, :, i] = 255 * ((img[:, :, i] - img[:, :, i].min()) / (img[:, :, i].max() - img[:, :, i].min()))
    
    return new_arr.astype(np.uint8)


def save_correct_arr(img_orig, img_add):
    new_img = np.zeros((*img_orig.shape, 4), dtype=np.uint8)
    for i in range(3):
        new_img[:, :, i] = img_orig
    new_img[:, :, 3] = 255
    img_normalized = normalize_img(new_img)
    img_normalized[new_img != img_add] = normalize_img(img_add)[new_img != img_add]
    return img_normalized
    


def __compare2arr(arr1, arr2):
    return np.sum((arr1[:, :, 0] == arr2[0]) & (arr1[:, :, 1] == arr2[1]) & (arr1[:, :, 2] == arr2[2]))
    

def draw_polygons_on_last_figure(last_figure: list, original_img: np.ndarray, 
                                 marker_class_1: list, alpha: float, return_annotation_info: bool = False, json_data = None):
    img_with_pathes = draw_annotations(original_img, marker_class_1)
    img_add = get_weight_image(img_with_pathes, original_img, alpha=alpha)
    c_img =img_add #save_correct_arr(original_img, img_add)
    plt.imsave('tmp.png', c_img)
    with open('tmp.png', 'rb') as f:
        last_figure['data'][0]['source'] = f'data:image/png;base64,{base64.b64encode(f.read()).decode()}'
    if not return_annotation_info:
        return last_figure
    
    data = json_data['small_image']['relative']
    x0, y0 = data['h0'], data['w0']
    x1, y1 = x0 + data['h'], y0 + data['w']
    img = img_with_pathes[x0:x1, y0:y1]
    annotation_info = {
        'class_1': __compare2arr(img, ANNOTATION_COLOR_CLASS_1),
        'class_0': __compare2arr(img, ANNOTATION_COLOR_CLASS_0),
    }
    # print(f'img_with_pathes shape = {img_with_pathes.shape}')
    # img_with_pathes[img_with_pathes == ANNOTATION_COLOR_CLASS_1] = 255 #[255, 255, 255]
    # img_with_pathes[img_with_pathes == ANNOTATION_COLOR_CLASS_0] = 0 #[0, 0, 0]
    # plt.imsave('tmp22.png', img_with_pathes)
    # print('HEREHRHERHEHR!`')
    return last_figure, annotation_info


def delete_polygons_on_last_figure(last_figure: list, original_img: np.ndarray):
    plt.imsave('tmp.png', original_img, cmap='gray')
    with open('tmp.png', 'rb') as f:
        last_figure['data'][0]['source'] = f'data:image/png;base64,{base64.b64encode(f.read()).decode()}'
    return last_figure



def draw_annotations(_img: np.ndarray, data: dict):
    """
        convert image to 3 channels, extract pathes and draw all selected classes on image including background
    """

    # draw pathes
    data_pathes = []
    for el in data:
        if el["type"] == "path":
            data_pathes.append(el)

    img_with_pathes = draw_pathes(_img, data_pathes)
    return img_with_pathes



def draw_pathes(_img: np.ndarray, data: list[dict], accurate: bool = False) -> np.ndarray:
    """
        Draw all selected classes on image
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

    for i, cnt in enumerate(contour):
        if data[i]["selected_class"] == 1:
            if accurate: cv2.fillConvexPoly(img, points=cnt, color=ANNOTATION_COLOR_CLASS_1, lineType=cv2.LINE_8)
            cv2.fillPoly(img, pts=[cnt], color=ANNOTATION_COLOR_CLASS_1, lineType=cv2.LINE_8)
        elif data[i]["selected_class"] == 0:
            if accurate: cv2.fillConvexPoly(img, points=cnt, color=ANNOTATION_COLOR_CLASS_0, lineType=cv2.LINE_8)
            cv2.fillPoly(img, pts=[cnt], color=ANNOTATION_COLOR_CLASS_0, lineType=cv2.LINE_8)
        else:
            print('ERRRRRORRR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    return img     
    
    
    
def get_weight_image(img: np.ndarray, img_orig: np.ndarray, alpha: float = 0.8):
    # change channels if needed
    # if len(img_orig.shape) == 2:
    #     new_img = np.zeros((*img_orig.shape, 4), dtype=np.uint8)
    #     for i in range(3):
    #         new_img[:, :, i] = img_orig
    #     new_img[:, :, -1] = 255
    #     _img_orig = new_img
    # else:   _img_orig = np.copy(img_orig)
    _img_orig = np.copy(img_orig)
    print(f'INPUT IMAGE SHAPE = {img.shape}; ORIG IMAGE SHAPE = {_img_orig.shape}')
    beta = 1-alpha
    gamma = 0
    img_add = cv2.addWeighted(_img_orig, alpha, img, beta, gamma)
    return img_add


##### SAVE FILE PAGE

def draw_annotated_image(_img: np.ndarray, data: dict, json_data: dict) -> np.ndarray:
    """
        draw binary annotated image
        data: selected_markers_   - array with pathes
    """
    img = np.copy(_img)

    data_pathes = []
    for el in data:
        if el["type"] == "path":
            data_pathes.append(el)

    # stencil = np.zeros(img.shape[:2], dtype=np.float64)
    stencil = draw_pathes(img, data_pathes)#draw_pathes_another(img, data_pathes)

    
    annotated_img = np.zeros((img.shape[0], img.shape[1]))
    annotated_img[(stencil == ANNOTATION_COLOR_CLASS_1)[:, :, 0]] = 255
    annotated_img[(stencil == ANNOTATION_COLOR_CLASS_0)[:, :, 0]] = 128

    position = json_data['small_image']['relative']
    h0, w0 = position['h0'], position['w0']
    h, w = position['h'], position['w']
    annotated_img = annotated_img[h0:h0+h, w0:w0+w]
    print(f'CUTTED IMG SIZE = {annotated_img.shape}')
    
    return annotated_img