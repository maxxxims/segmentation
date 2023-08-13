import numpy as np
from PIL import Image as IMG
import matplotlib.pyplot as plt
from image.markers import Marker, MarkerContainer
from filters.filters import BaseFilter2D


class Image:
    def __init__(self, path_to_image: str = '',  dim: int = 2, **kwargs: str) -> None:
        if 'data' in kwargs.keys():
            self.data_raw = kwargs.get('data')
            self.data = kwargs.get('data')
            self.dim = kwargs.get('data').shape
            return None
        self.dim = dim
        if dim == 2:
            with IMG.open(path_to_image) as img:
                img.load()
                self.data_raw = np.array(img)
                self.data = np.array(img)
                #self.data = img
                

    # def apply_filter(self, filter: callable, **kwargs):
    #     self.data = filter(np.array(self.data), **kwargs)
    def apply_filter(self, *filters: BaseFilter2D):
        for filter in filters:
            filter.change_image(self)


    def draw_marker(self, markers: MarkerContainer|Marker) -> None:
        markers.draw(self.data)


    def set_image(self, new_data: np.array):
        self.data = new_data
        

    def get_image(self):
        return self.data
    

    def histogram(self):
        plt.hist(self.data.ravel(), range=[0, 256], bins=256)
        plt.show()


    def show(self, show_original: bool = False):
        #IMG.fromarray(self.data).convert('P').show()
        if show_original:
            self._show(self.data_raw)
        else:
            self._show(self.data)

    def show_segmentation(self):
        t = np.copy(self.data_raw)
        t[self.data == 0] = 0
        self._show(t)

    
    def show_segments(self, marker: Marker):
        t = np.copy(self.data_raw)
        value = self.data[marker.x1, marker.y1]
        print(f'value = {value}')
        t[self.data == value] = 0
        self._show(t)


    def shape(self):
        return self.data.shape
    

    def dim(self):
        return self.dim
    

    def _show(self, data, **kwargs):
        plt.imshow(data, cmap='gray', **kwargs)
        plt.show()
    
