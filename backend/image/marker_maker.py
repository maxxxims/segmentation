import matplotlib.pyplot as plt
from PIL import Image as IMG
import numpy as np
from ..image import MarkerContainer, Marker, MarkerFill2D


class MarkerMaker:
    """
        from piece of segmented image make markers for segmentation 
    """
    pass



class MarkerMakerRectangle2DBinary(MarkerMaker):
    """
        from piece of segmented image make markers for segmentation 
    """
    def __init__(self, path_to_image: str, x1: int, y1: int, x4: int, y4: int) -> None:
        super().__init__()
        self.path_to_image = path_to_image
        self.threshold = 255
        self.x1 = x1
        self.y1 = y1
        self.x4 = x4
        self.y4 = y4

    def _load_slice(self) -> np.ndarray:
        """
            open img and load slice
        """
        with IMG.open(self.path_to_image) as img:
            img.load()
        return np.array(img)
    

    def get_markers(self) -> MarkerContainer:
        """
            make markers from sliced image
        """
        orig_img   = self._load_slice()
        sliced_img = orig_img[self.y1:self.y4, self.x1:self.x4]

        class_1 = np.where(sliced_img >= self.threshold)
        class_0 = np.where(sliced_img < self.threshold)
        print(f'shape class_1 = {class_1[0].shape}')
        print(f'shape class_0 = {class_0[0].shape}')
        # print(len)
        
        marker_list = []

        if len(class_0[0]) != 0:
            class_0_index = np.vstack((class_0[1] + self.x1, class_0[0] + self.y1)).T.ravel()
            marker_list.append(MarkerFill2D(points=class_0_index, value=0))
        if len(class_1[0]) != 0:
            class_1_index = np.vstack((class_1[1] + self.x1, class_1[0] + self.y1)).T.ravel()
            marker_list.append(MarkerFill2D(points=class_1_index, value=1))

        #class_1_index = np.vstack((class_1[1] + self.x1, class_1[0] + self.y1)).T.ravel()
        #class_0_index = np.vstack((class_0[1] + self.x1, class_0[0] + self.y1)).T.ravel()

        markers = MarkerContainer(marker_list)


        # markers = MarkerContainer(markers=
        #                           [MarkerFill2D(points=class_1_index, value=1), 
        #                            MarkerFill2D(points=class_0_index, value=0)], dim=2
        #                         ) 
        return markers


    def show_slice(self):
        """
            show slice of segmented image
        """
        img = self._load_slice()
        plt.imshow(img, cmap='gray')
        plt.show()

        plt.imshow(img[self.y1:self.y4, self.x1:self.x4], cmap='gray')
        plt.show()
