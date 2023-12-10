import numpy as np
from skimage.transform import resize, rescale


class BaseFilter2D:
    dim = 2
    def __init__(self, scale: int = 1, **kwargs: dict) -> None:
        self.filter = lambda data: data
        self.name = f'Base Filter scale={scale}'
        self.params = kwargs
        self.scale = scale
    
    def change_image(self, image) -> None:
        """
            change img data
        """
        if self.scale == 1:
            image.data = self.filter(image.data, **self.params)
        else:
            image.data = 255 * resize(image=self.filter(image.data[::self.scale, ::self.scale], **self.params),
                                output_shape=image.shape)

    
    def make_mask(self, image) -> np.array:
        """
            return changed img data
        """
        if self.scale == 1:
            return self.filter(image.data, **self.params)
        else:
            old_shape = image.shape
            data = self.filter(image.data[::self.scale, ::self.scale], **self.params)
            coef = 255
            if np.max(data) <= 1:
                coef = 255
                
            # print(np.max(data), coef)
            result = coef * resize(data, output_shape=old_shape)
            # print(f'max result {np.max(result)}')
            return  result



class BaseFilter3D:
    dim = 3
    def __init__(self, scale: int = 1, **kwargs: dict) -> None:
        self.filter = lambda data: data
        self.name = f'Base Filter scale={scale}'
        self.params = kwargs
        self.scale = scale
    
    def change_image(self, image) -> None:
        """
            change img data
        """
        if self.scale == 1:
            image.data = self.filter(image.data, **self.params)
        else:
            image.data = 255 * resize(image=self.filter(image.data[::self.scale, ::self.scale, ::self.scale], **self.params),
                                output_shape=image.shape)

    
    def make_mask(self, image) -> np.array:
        """
            return changed img data
        """
        if self.scale == 1:
            return self.filter(image.data, **self.params)
        else:
            old_shape = image.shape
            data = self.filter(image.data[::self.scale, ::self.scale, ::self.scale], **self.params)
            coef = 255
            if np.max(data) <= 1:
                coef = 255
            result = coef * resize(data, output_shape=old_shape)
            print(f'max result = {np.max(result)}')
            return  result