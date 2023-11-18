import numpy as np
from ..image import Image, Marker



class Image3D:
    def __init__(self, img_pathes: list[str], batch_size: int = 10) -> None:
        self.img_pathes = img_pathes.copy()
        self.data = np.array([[[]]])
        self.__img_indexes  = []

        self.batch_number = 0
        self.imges_number = len(self.img_pathes)
        self.batch_size   = min(batch_size, self.imges_number)

        temp_img = Image(path_to_image=self.img_pathes[0])
        self.__shape = (len(self.img_pathes), temp_img.height, temp_img.width)
  


    def load_batch(self, batch_number: int) -> bool:
        """
            :param batch_number: number of batch to load. Images indexes < batch_number * batch_size
            :return: True if last batch was loaded, False if not enough images
        """
        last_img_number = min(batch_number * self.batch_size, self.imges_number)
        if last_img_number > self.imges_number:
            return False
        
        self.batch_number = batch_number
        self.clear_cache()
        self.load_images(indx_start=(self.batch_number - 1) * self.batch_size, indx_end=last_img_number - 1)
        # self.data = [
        #     Image(path_to_image=self.img_pathes[i]).data for i in range((self.batch_number - 1) * self.batch_size, last_img_number)
        # ]
        # self.__img_indexes = list(range((self.batch_number - 1) * self.batch_size, last_img_number))
        assert len(self.data) == len(self.img_indexes), f'{len(self.data)} != {len(self.img_indexes)}'
        return True

    def show(self, indx: int, show_original: bool = False):
        """
            :param indx: index of 2d image
            :param show_original: if True show original image from directory
        """
        assert indx < self.__len__(), "Out of range"
        if show_original:
            Image(path_to_image=self.img_pathes[indx]).show()
        else:
            self[indx].show()


    def draw_marker(self, marker: Marker, color: int = 255):
        
        marker.draw(self.data, color=color)

    def load_images(self, indx_start: int, indx_end: int):
        """
            Load images and images' indexes from indx_start to indx_end and append to data.
            Index start from 0
        """
        self.__img_indexes = list(range(indx_start, indx_end + 1))
        # self.data = np.concatenate(
        #     (self.data, [Image(path_to_image=self.img_pathes[i]).data for i in range(indx_start, indx_end + 1)]),
            
        #     )
        self.data = np.array([Image(path_to_image=self.img_pathes[i]).data for i in range(indx_start, indx_end + 1)])
        assert len(self.data) == len(self.img_indexes), f'{len(self.data)} != {len(self.img_indexes)}'
        return True


    def clear_cache(self, save_data: bool = False):
        del self.data, self.__img_indexes
        self.data = np.array([[[]]])
        self.__img_indexes = []


    @property
    def shape(self) -> tuple[int, int, int]:
        return self.__shape
    

    @property
    def len_loaded_images(self) -> int:
        assert len(self.data) == len(self.__img_indexes), f'{len(self.data)} != {len(self.__img_indexes)}'
        return len(self.img_indexes)
    

    @property
    def img_indexes(self) -> list[int]:
        return self.__img_indexes.copy()

    
    def _load_img(self, indx: int):
        img_path = self.img_pathes[indx]
        img = Image(path_to_image=img_path).data
        return img

    def __len__(self) -> int:
        return self.shape[0]

    def __getitem__(self, indx: int) -> Image:
        if indx < 0:
            indx = self.imges_number + indx
        if indx < 0 or indx >= self.imges_number:
            raise IndexError
        
        if indx in self.__img_indexes:
            return Image(data=self.data[self.__img_indexes.index(indx)])
        else:
            return Image(data=self._load_img(indx))