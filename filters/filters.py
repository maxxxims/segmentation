import numpy as np
from PIL import Image as IMG
from PIL import ImageFilter

def test(data: np.array):
    x_size, y_size = data.shape
    data[x_size//4 : 3*x_size//4, y_size//4 : 3*y_size//4] = 255
    return data

def threshold(data: np.array, threshold: int):
    return data > threshold


def MinFilter(data: np.array, times: int = 1, size: int = 3):
    img = IMG.fromarray(data)
    for i in range(times):
        img = img.filter(ImageFilter.MinFilter(size))
    return np.array(img)


def MaxFilter(data: np.array, times: int = 1, size: int = 3):
    img = IMG.fromarray(data)
    for i in range(times):
        img = img.filter(ImageFilter.MaxFilter(size))
    return np.array(img)