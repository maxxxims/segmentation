import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from svg.path import parse_path, path
from .save_annotation import draw_pathes as draw_pathes_another, MASK_VALUE
import base64
import io


N_POINTS = int(1e3)
ANNOTATION_COLOR = (0, 255, 0, 0)

ANNOTATION_COLOR_BG = (150, 10, 0, 0)

# MASK_VALUE = 255


def __bytes_to_image_pil(byte_data):
    image = Image.open(io.BytesIO(byte_data))
    return image

def draw_polygons_on_last_figure(last_figure: list, original_img: np.ndarray, marker_class_1: list, reverse: bool, alpha: float):
    content = last_figure['data'][0]['source']
    content_type, content_string = content.split(',')
    byte_data = base64.b64decode(content_string)
    img = np.asanyarray(Image.open(io.BytesIO(byte_data)))
    img_add, _ = draw_annotations(original_img, marker_class_1, reverse=reverse, alpha=alpha)
    plt.imsave('tmp.png', img_add)
    with open('tmp.png', 'rb') as f:
        last_figure['data'][0]['source'] = f'data:image/png;base64,{base64.b64encode(f.read()).decode()}'
    return last_figure


def delete_polygons_on_last_figure(last_figure: list, original_img: np.ndarray):
    plt.imsave('tmp.png', original_img, cmap='gray')
    with open('tmp.png', 'rb') as f:
        last_figure['data'][0]['source'] = f'data:image/png;base64,{base64.b64encode(f.read()).decode()}'
    return last_figure
    


def draw_annotated_image(_img: np.ndarray, data: dict, selected_class: int) -> np.ndarray:
    """
        data: selected_markers_   - array with pathes
    """
    selected_class = int(selected_class)
    img = np.copy(_img)

    data_pathes = []
    for el in data:
        if el["type"] == "path":
            data_pathes.append(el)


    stencil = draw_pathes_another(img, data_pathes)
    if selected_class == 1:
        select = stencil == MASK_VALUE
        select_bg = stencil != MASK_VALUE

    else:
        select = stencil != MASK_VALUE
        select_bg = stencil == MASK_VALUE
    
    annotated_img = np.zeros((img.shape[0], img.shape[1]))
    annotated_img[select] = 255

    return annotated_img



def draw_annotations(_img: np.ndarray, data: dict, reverse: bool = False, alpha: float = 0.8):
    """
        if reverse: draw background
    """
    print(f'*********************8 reverse = {reverse}')

    # change channels if needed
    if len(_img.shape) == 2:
        new_img = np.zeros((*_img.shape, 4), dtype=np.uint8)
        for i in range(3):
            new_img[:, :, i] = _img
        new_img[:, :, -1] = 255
        _img = new_img
    # print(f'IMAGE SHAPE = {_img.shape}')

    # draw pathes
    data_pathes = []

    for el in data:
        if el["type"] == "path":
            data_pathes.append(el)

    img_add, img = draw_pathes(_img, data_pathes, reverse=reverse, alpha=alpha)
    return img_add, img


def draw_figures(_img: np.ndarray, data: list[dict], reverse: bool = False):
    """
        Not emplemented
    """
    img_orig = np.copy(_img)
    img = np.copy(_img)
    for el in data:
        if el['type'] == 'rectangle':
            cv2.rectangle(img, (el['x0'], el['y0']), (el['x1'], el['y1']), ANNOTATION_COLOR, 1)
    ...


def draw_pathes(_img: np.ndarray, data: list[dict], reverse: bool = False, alpha: float = 0.8):
    """_summary_

    Args:
        _img (np.ndarray): _description_
        data (list[dict]): _description_
        reverse (bool, optional): _description_. Defaults to False.
        alpha (float, optional): _description_. Defaults to 0.8.

    Returns:
        _type_: _description_
    """
    # print(f'reverse = {reverse}')
    img_orig = np.copy(_img)
    img = np.copy(_img)

    n_polygons = len(data)
    pathes_arr = [parse_path(data[j]["path"]) for j in range(n_polygons)]
    # pth = parse_path(data["path"])

    contour = [[] for _ in range(n_polygons)]

    for i in range(N_POINTS):
        for j in range(n_polygons):
            point = pathes_arr[j].point(i / N_POINTS)
            x, y = round(np.real(point)), round(np.imag(point))
            contour[j].append(np.array([[x, y]]))

    contour = np.array(contour)

    stencil = np.zeros(img.shape[:2], dtype=np.uint8)
    for cnt in contour:
        cv2.NONE_POLISHER
        #cv2.drawContours(stencil, cnt, contourIdx=-1, color=MASK_VALUE,thickness=cv2.FILLED)
        cv2.fillPoly(stencil, pts=[cnt], color=MASK_VALUE, lineType=cv2.LINE_8) #, fillrule='nonzero'
    if not reverse:
        select = stencil == MASK_VALUE
        img[select] = ANNOTATION_COLOR
    else:
        # select = stencil == MASK_VALUE
        # select_bg = stencil != MASK_VALUE
        # img[select_bg] = ANNOTATION_COLOR_BG
        # img[select] = ANNOTATION_COLOR
        select = stencil != MASK_VALUE
        img[select] = ANNOTATION_COLOR


    # cv2.fillPoly(img, pts=contour, color=ANNOTATION_COLOR)


    # return img with polygons
    # alpha = 0.8
    beta = 1-alpha
    gamma = 0

    img_add = cv2.addWeighted(img_orig, alpha, img, beta, gamma)

    # plt.title('orig image')
    # plt.imshow(img)
    # plt.show()
    # plt.imshow(img_add)
    # plt.show()
    # print(img_add.shape, img.shape)
    return img_add, img



