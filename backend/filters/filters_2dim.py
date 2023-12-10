import numpy as np
from PIL import Image as IMG
from PIL import ImageFilter
from .filters import BaseFilter2D
from ..image import Image
from scipy.ndimage import gaussian_filter, median_filter, laplace, variance, convolve



class Threshold(BaseFilter2D):
    def __init__(self, threshold: int) -> None:
        super().__init__(threshold=threshold)
        def filter_work(data: np.ndarray, threshold: int) -> np.array:
            temp = np.copy(data)
            temp[data > threshold] = 255
            temp[data <= threshold] = 0
            return temp
        self.filter = filter_work
        self.name = f'Threshold Filter threshold={threshold}'
        

class MinFilter(BaseFilter2D):
    def __init__(self, size: int, times: int = 1) -> None:
        super().__init__(size=size, times=times)
        def filter_work(data: np.ndarray, size: int, times: int = 1) -> np.array:
            img = IMG.fromarray(data)
            for i in range(times):
                img = img.filter(ImageFilter.MinFilter(size))
            return np.array(img)
        self.filter = filter_work
        self.name = 'Min Filter'


class MaxFilter(BaseFilter2D):
    def __init__(self, size: int, times: int = 1) -> None:
        super().__init__(size=size, times=times)
        def filter_work(data: np.ndarray,size: int, times: int) -> np.array:
            img = IMG.fromarray(data)
            for i in range(times):
                img = img.filter(ImageFilter.MaxFilter(size))
            return np.array(img)
        self.filter = filter_work
        self.name = 'Max Filter'


class GaussianFilter(BaseFilter2D):
    def __init__(self, sigma: int, scale: int = 1) -> None:
        super().__init__(scale, sigma=sigma)
        def filter_work(data: np.ndarray, sigma: int) -> np.array:
            return gaussian_filter(data, sigma=sigma)
        self.filter = filter_work
        self.name = f'Gaussian Filter sigma={sigma} scale={scale}'


class MedianFilter(BaseFilter2D):
    def __init__(self, size: int, scale: int = 1) -> None:
        super().__init__(scale, size=size)
        def filter_work(data: np.ndarray, size: int) -> np.array:
            return median_filter(data, size=size)
        self.filter = filter_work
        self.name = f'Median Filter size={size} scale={scale}'


class HighPassFilter(BaseFilter2D):
    def __init__(self, k: int = 1, scale: int = 1) -> None:
        super().__init__(scale, k=k)
        def filter_work(data: np.ndarray, k: int) -> np.array:
            kernel = np.array([
                    [0, -1, 0],
                    [-1, 4, -1],
                    [0 , -1, 0]
            ]) / k
            return convolve(data, kernel)
        self.filter = filter_work
        self.name = f'High Pass Filter k={k} scale={scale}'



class LowPassFilter(BaseFilter2D):
    def __init__(self, size: int = 3, scale: int = 1) -> None:
        super().__init__(scale, size=size)
        def filter_work(data: np.ndarray, size: int) -> np.array:
            kernel = np.ones((size, size)) / (size * size)
            return convolve(data, kernel)
        self.filter = filter_work
        self.name = f'Low Pass Filter size={size} scale={scale}'


class LaplacianDifference(BaseFilter2D):
    def __init__(self, scale: int = 1) -> None:
        super().__init__(scale)
        def filter_work(data: np.ndarray) -> np.array:
            return laplace(data)
        self.filter = filter_work
        self.name = f'Laplacian Difference scale={scale}'


"""
win_mean = ndimage.uniform_filter(img, (win_rows, win_cols))
win_sqr_mean = ndimage.uniform_filter(img**2, (win_rows, win_cols))
win_var = win_sqr_mean - win_mean**2
"""

class VarianceFilter(BaseFilter2D):
    def __init__(self, size: int, scale: int = 1) -> None:
        super().__init__(scale, size=size)
        def filter_work(data: np.ndarray, size: int) -> np.array:
            img_mean = convolve(data, np.ones((size, size)) / size **2)
            if size % 2 == 0:   size += 1
            e = np.zeros((size, size))
            e[size // 2, size // 2] = 1
            sigma = convolve((data - img_mean) ** 2, weights= (e / size**2) )
            return np.sqrt(sigma.astype(np.float64))
        self.filter = filter_work
        self.name = f'Variance Filter scale={scale}'


class ColorScale(BaseFilter2D):
    def __init__(self, scale: int = 1) -> None:
        super().__init__(scale)
        def filter_work(data: np.ndarray) -> np.array:
            mn, mx = np.min(data), np.max(data)
            print(mn,mx)
            temp = np.copy(data)   
            temp =  255 * (temp - mn) / (mx - mn)
            print(temp)
            return temp
        self.filter = filter_work
        self.name = f'Color scale scale={scale}'


   ##########################################
  #        Morphological Filters           #
 ##########################################

from skimage.morphology import erosion, dilation, opening, closing
from skimage.morphology import square


class Erosion(BaseFilter2D):
    def __init__(self, size: int, structure_element = None, scale: int = 1) -> None:
        super().__init__(scale, size=size)
        def filter_work(data: np.ndarray, size: int) -> np.array:
            structure_element = square(size)
            return erosion(data, structure_element)
        self.filter = filter_work
        self.name = f'Erosion 2D scale={scale}'


class Dilation(BaseFilter2D):
    def __init__(self, size: int, structure_element = None, scale: int = 1) -> None:
        super().__init__(scale, size=size)
        def filter_work(data: np.ndarray, size: int) -> np.array:
            structure_element = square(size)
            return dilation(data, structure_element)
        self.filter = filter_work
        self.name = f'Dilation 2D scale={scale}'


class Opening(BaseFilter2D):
    def __init__(self, size: int, structure_element = None, scale: int = 1) -> None:
        super().__init__(scale, size=size)
        def filter_work(data: np.ndarray, size: int) -> np.array:
            structure_element = square(size)
            return opening(data, structure_element)
        self.filter = filter_work
        self.name = f'Opening 2D scale={scale}'


class Closing(BaseFilter2D):
    def __init__(self, size: int, structure_element = None, scale: int = 1) -> None:
        super().__init__(scale, size=size)
        def filter_work(data: np.ndarray, size: int) -> np.array:
            structure_element = square(size)
            return closing(data, structure_element)
        self.filter = filter_work
        self.name = f'Closing 2D scale={scale}'