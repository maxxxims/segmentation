import numpy as np
from PIL import Image as IMG
import matplotlib.pyplot as plt
from ..image.markers import Marker
from ..filters.filters import BaseFilter2D
from typing import Any
class Image:
    def __init__(self, path_to_image: str = '', **kwargs: Any) -> None:
        """ 
            :kwargs data: if passed make img from array
        """
        if 'data' in kwargs.keys():
            self.data_raw = kwargs.get('data')
            self.data = kwargs.get('data')
            self.max_color = np.max(self.data)
        else:
            with IMG.open(path_to_image, 'r') as img:
                img.load()
                self.data_raw = np.array(img)
                self.data = np.copy(self.data_raw)
                self.max_color = np.max(self.data)
        
        shape = self.data.shape
        self.__height, self.__width = shape[0], shape[1]


    def apply_filter(self, *filters: BaseFilter2D):
        for filter in filters:
            filter.change_image(self)


    def draw_marker(self, markers: Marker, color: int = 255) -> None:
        markers.draw(self.data, color=color)


    def set_image(self, new_data: np.array):
        self.data = new_data
    

    def reset(self) -> None:
        self.data = np.copy(self.data_raw)
        

    def get_image(self):
        return self.data
    

    def histogram(self):
        plt.hist(self.data.ravel(), range=[0, 256], bins=256)
        plt.show()


    def show(self, show_original: bool = False, title: str = None):
        if show_original:
            self._show(self.data_raw, title='original image')
        else:
            self._show(self.data, title=title)

    def save(self, path_to_save: str):
        plt.imsave(path_to_save, self.data, cmap='gray')


    def show_segmentation(self):
        t = np.copy(self.data_raw)
        t[self.data == 0] = 0
        self._show(t)

    
    def show_segments(self, marker: Marker, mask = None, fill_color: int = 0):
        if not mask:
            value = self.data[marker.y1, marker.x1]
        else: 
            value = mask.data[marker.y1, marker.x1]
        t = np.copy(self.data_raw)    
        print(f'marker class = {marker.value}')
        t[self.data != value] = fill_color
        self._show(t)


    @property
    def shape(self) -> tuple:
        return self.data.shape
    
    @property
    def height(self):
        return self.__height
    
    @property
    def width(self):
        return self.__width

    def _show(self, data, title: str = None, **kwargs):
        plt.figure(figsize=(10, 10))
        if title:
            plt.title(title)
        plt.imshow(data, cmap='gray', **kwargs)
        plt.show()
    

    