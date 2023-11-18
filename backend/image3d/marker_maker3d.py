from ..image import MarkerMaker
import matplotlib.pyplot as plt
from PIL import Image as IMG
import numpy as np
from ..image import MarkerContainer, Marker, MarkerFill2D
# from .image3d import MarkerPoints3D
from .markers3d import MarkerPoints3D
from .image3d import Image3D


class MarkerMaker3DBinary(MarkerMaker):
    """
        from piece of segmented 3D image make markers for segmentation 
    """
    def __init__(self, x1: int, y1: int, z1: int,
                   x8: int, y8: int, z8: int) -> None:
        super().__init__()
        self.threshold = 255
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1
        self.x4 = x8
        self.y4 = y8
        self.z4 = z8
    
    def get_markers(self, image) -> MarkerContainer:
        """
            make markers from sliced image
        """
        sliced_img   = self._load_slice(image)

        class_1 = np.where(sliced_img >= self.threshold)
        class_0 = np.where(sliced_img < self.threshold)

        # print(
        #     max(class_1[0]), max(class_1[1]), max(class_1[2]),
        # )

        print(f'instances of class 1 = {class_1[0].shape}')
        print(f'instances of class 0 = {class_0[0].shape}')
    
        marker_list = []

        if len(class_0[0]) != 0:
            # class_0_index = np.vstack((class_0[1] + self.x1, class_0[0] + self.y1,
            #                            class_0[2] + self.z1)).T.ravel()
            x_index = class_0[2] + self.x1
            y_index = class_0[1] + self.y1
            z_index = class_0[0] + self.z1
            marker_list.append(MarkerPoints3D(x_indexes=x_index, y_indexes=y_index, z_indexes=z_index,
                                              value=0))
            
        if len(class_1[0]) != 0:
            # class_1_index = np.vstack((class_1[1] + self.x1, class_1[0] + self.y1,
            #                            class_1[2] + self.z1)).T.ravel()
            x_index = class_1[2] + self.x1
            y_index = class_1[1] + self.y1
            z_index = class_1[0] + self.z1
            marker_list.append(MarkerPoints3D(x_indexes=x_index, y_indexes=y_index, z_indexes=z_index,
                                              value=1))
            
        markers = MarkerContainer(marker_list)
        return markers

    def _load_slice(self, image) -> np.ndarray:
        """
            open img and load slice
        """
        image.clear_cache(save_data=False)
        image.load_images(self.z1, self.z4)
        return image.data[self.z1:self.z4, self.y1:self.y4, self.x1:self.x4]
   

    def show_slice(self):
        """
            show slice of segmented image
        """
        img = self._load_slice()
        plt.imshow(img, cmap='gray')
        plt.show()

        plt.imshow(img[self.y1:self.y4, self.x1:self.x4], cmap='gray')
        plt.show()
