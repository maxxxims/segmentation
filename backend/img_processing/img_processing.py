import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from svg.path import parse_path, path
from .save_annotation import draw_pathes as draw_pathes_another, MASK_VALUE


N_POINTS = int(1e3)
ANNOTATION_COLOR = (0, 255, 0, 0)

ANNOTATION_COLOR_BG = (150, 10, 0, 0)

# MASK_VALUE = 255




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



def draw_annotations(_img: np.ndarray, data: dict, reverse: bool = False):
    """
        if reverse: draw background
    """
    

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

    img_add, img = draw_pathes(_img, data_pathes, reverse=reverse)
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


def draw_pathes(_img: np.ndarray, data: list[dict], reverse: bool = False):
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
        cv2.fillPoly(stencil, pts=[cnt], color=MASK_VALUE) #, fillrule='nonzero'
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
    alpha = 0.8
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



