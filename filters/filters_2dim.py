import numpy as np
from PIL import Image as IMG
from PIL import ImageFilter
from filters.filters import BaseFilter2D
from image.image import Image

class Threshold(BaseFilter2D):
    def __init__(self, threshold: int) -> None:
        super().__init__()
        def filter_work(image: Image) -> np.array:
            temp = image.data
            temp[image.data > threshold] = 255
            temp[image.data <= threshold] = 0
            #image.data > threshold
            return temp
        self.filter = filter_work
        self.name = 'Threshold Filter'

class MinFilter(BaseFilter2D):
    def __init__(self, size: int, times: int = 1) -> None:
        super().__init__()
        def filter_work(image: Image, size: int, times: int = 1) -> np.array:
            img = IMG.fromarray(image.data)
            for i in range(self.times):
                img = img.filter(ImageFilter.MinFilter(self.size))
            return np.array(img)
        self.filter = filter_work
        self.name = 'Min Filter'


class MaxFilter(BaseFilter2D):
    def __init__(self, size: int, times: int = 1) -> None:
        super().__init__()
        def filter_work(image: Image) -> np.array:
            img = IMG.fromarray(image.data)
            for i in range(times):
                img = img.filter(ImageFilter.MaxFilter(size))
            return np.array(img)
        self.filter = filter_work
        self.name = 'Max Filter'


class ColorScale(BaseFilter2D):
    def __init__(self) -> None:
        super().__init__()
        def filter_work(image: Image) -> np.array:
            mn, mx = np.min(image.data), np.max(image.data)
            print(mn,mx)
            temp = np.copy(image.data)   
            temp =  255 * (temp - mn) / (mx - mn)
            print(temp)
            return temp
        self.filter = filter_work
        self.name = 'Color scale'