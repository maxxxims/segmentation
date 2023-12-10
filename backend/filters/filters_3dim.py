import numpy as np
from PIL import Image as IMG
from PIL import ImageFilter
from .filters import BaseFilter3D
from ..image import Image
from scipy.ndimage import gaussian_filter, median_filter, laplace, variance, convolve



class GaussianFilter(BaseFilter3D):
    def __init__(self, sigma: int, scale: int = 1) -> None:
        super().__init__(scale, sigma=sigma)
        def filter_work(data: np.ndarray, sigma: int) -> np.ndarray:
            return gaussian_filter(data, sigma=sigma)
        self.filter = filter_work
        self.name = f'Gaussian Filter sigma={sigma} scale={scale}'


class MedianFilter(BaseFilter3D):
    def __init__(self, size: int, scale: int = 1) -> None:
        super().__init__(scale, size=size)
        def filter_work(data: np.ndarray, size: int) -> np.ndarray:
            return median_filter(data, size=size)
        self.filter = filter_work
        self.name = f'Median Filter size={size} scale={scale}'


class LaplacianDifference(BaseFilter3D):
    def __init__(self, scale: int = 1) -> None:
        super().__init__(scale)
        def filter_work(data: np.ndarray) -> np.ndarray:
            return laplace(data)
        self.filter = filter_work
        self.name = f'Laplacian Difference scale={scale}'


class VarianceFilter(BaseFilter3D):
    def __init__(self, size: int, scale: int = 1) -> None:
        super().__init__(scale, size=size)
        size = size
        def filter_work(data: np.ndarray, size: int) -> np.array:
            img_mean = convolve(data, np.ones(shape=(size, size, size)) / size **3)
            if size % 2 == 0:   size += 1
            e = np.zeros((size, size, size))
            e[size // 2, size // 2, size // 2] = 1
            sigma = convolve((data - img_mean) ** 2, e / size**3 )
            return np.sqrt(sigma.astype(np.float64)).astype(np.float64)
        self.filter = filter_work
        self.name = f'Variance Filter size={size} scale={scale}'
