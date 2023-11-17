from PIL import Image as IMG
import numpy as np
from ..image import Image



class Image3D:
    def __init__(self, img_pathes: list[str], batch_size: int = 10) -> None:
        self.img_pathes = img_pathes
        self.data = []
        self.__img_indexes  = []
        self.batch_number = 0
        self.imges_number = len(self.img_pathes)
        self.batch_size   = min(batch_size, self.imges_number)


    def load_batch(self, batch_number: int) -> bool:
        """
            :param batch_number: number of batch to load. Images indexes < batch_number * batch_size
            :return: True if last batch was loaded, False if not enough images
        """
        last_img_number = min(batch_number * self.batch_size, self.imges_number)
        if last_img_number > self.imges_number:
            return False
        
        self.batch_number = batch_number
        del self.data, self.__img_indexes
        self.data = [
            Image(path_to_image=self.img_pathes[i]).data for i in range((self.batch_number - 1) * self.batch_size, last_img_number)
        ]
        self.__img_indexes = list(range((self.batch_number - 1) * self.batch_size, last_img_number))
        assert len(self.data) == len(self.img_indexes), f'{len(self.data)} != {len(self.img_indexes)}'
        return True

    def show(self, indx: int, show_original: bool = False):
        """
            :param indx: index of 2d image
            :param show_original: if True show original image from directory
        """
        assert indx < self.imges_number, "Out of range"
        if show_original:
            Image(path_to_image=self.img_pathes[indx]).show()
        else:
            self.data[indx].show()


    def _load_img(self, indx: int):
        img_path = self.img_pathes[indx]
        img = Image(path_to_image=img_path).data
        # with IMG.open(img_path, 'r') as img:
        #     img.load()
        #     img = np.asarray(img, dtype=np.uint8)
        #     assert len(img.shape) == 2, f'{img.shape} != 2'
            # print('image shape', img.shape, np.asarray(img, dtype=np.uint8))
        return img
    

    def _load_images(self, indx_start: int, indx_end: int):
        """
            Load images and images' indexes from indx_start to indx_end.
            Index start from 0
        """
        self.__img_indexes += list(range(indx_start, indx_end + 1))
        self.data += [
            Image(path_to_image=self.img_pathes[i]).data for i in range(indx_start, indx_end + 1)
        ]
        assert len(self.data) == len(self.img_indexes), f'{len(self.data)} != {len(self.img_indexes)}'
        return True


    @property
    def len_loaded_images(self) -> int:
        assert len(self.data) == len(self.__img_indexes), f'{len(self.data)} != {len(self.__img_indexes)}'
        return len(self.img_indexes)
    

    @property
    def img_indexes(self) -> list[int]:
        return self.__img_indexes.copy()


    def __getitem__(self, indx: int) -> Image:
        if indx < 0:
            indx = self.imges_number + indx
        if indx < 0 or indx >= self.imges_number:
            raise IndexError
        
        if indx in self.__img_indexes:
            return Image(data=self.data[self.__img_indexes.index(indx)])
        else:
            return Image(data=self._load_img(indx))