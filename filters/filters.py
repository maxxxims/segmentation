import numpy as np

class BaseFilter2D:
    def __init__(self) -> None:
        self.dim = 2
        self.filter = lambda image: image.data

    
    def change_image(self, image) -> None:
        image.data = self.filter(image)

    
    def make_mask(self, image) -> np.array:
        return self.filter(image)