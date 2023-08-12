import numpy as np
from PIL import Image as IMG
import matplotlib.pyplot as plt


class Image:
    def __init__(self, path_to_image: str,  dim: int = 2) -> None:
        self.dim = dim
        if dim == 2:
            with IMG.open(path_to_image) as img:
                img.load()
                self.data = np.array(img)
                #self.data = img
                

    def apply_filter(self, filter: callable, **kwargs):
        self.data = filter(np.array(self.data), **kwargs)


    def _open_png(path_to_image: str):
        ...


    def get_image(self):
        return self.data
    

    def histogram(self):
        plt.hist(self.data.ravel(), range=[0, 256], bins=256)
        plt.show()


    def show(self):
        #IMG.fromarray(self.data).convert('P').show()
        plt.imshow(self.data, cmap='gray')
        plt.show()

    def shape(self):
        return self.data.shape
    

    def get_dim(self):
        return self.dim
    
