import numpy as np
from ..image import Image, Marker, MarkerContainer
from ..filters.filters import BaseFilter2D
import pandas as pd
from sklearn.utils import shuffle
from ..image3d import Image3D

class Segmentation3D:
    def __init__(self, model, filters: list[BaseFilter2D],
                 batch_size = 10, informing: bool = True) -> None:
        self.informing = informing
        self.batch_size = batch_size
        self.padding = 0
        self.__model = model
        self.__filters   = np.copy(filters)
        self.__filters_names = get_filters_names(filters)
        

    def fit(self, image: Image3D, markers: MarkerContainer,
            check: bool = False, features: np.ndarray = None):
        if features is None:
            image.clear_cache()
            image.load_images(indx_start=0, indx_end=self.batch_size - 1 + self.padding)
            features = self.apply_filters(image)
            print('features shape = ', np.shape(features))
        if self.informing: print('Making train data...')
        # get x_train and y_train
        class2data = {}
        y_train = []
        for m in markers:
            value = m.value
            x_indexes, y_indexes, z_indexes = m.get_indexes()
            class2data[value] = features[z_indexes, y_indexes, x_indexes]
            print(f'feature shape = {np.shape(features[z_indexes, y_indexes, x_indexes])}')
            y_train += [value] * len(x_indexes)

        x_train = np.concatenate([class2data[m.value] for m in markers])
        print(f'x_train shape = {np.shape(x_train)}, y_train shape = {np.shape(y_train)}')
        x_train, y_train = shuffle(x_train, y_train, random_state=42)

        if self.informing: print('Fitting model...')
        self.__model.fit(x_train, y_train)


    def predict(self, image: Image3D, features: np.ndarray = None) -> np.ndarray:
        """
            Segmentate image
        """
        if not features:
            features = self.apply_filters(image)
        if self.informing: print('Making predictions...')
        depth = len(image.data)
        preds = self.__model.predict(
            features.reshape((depth * image.height * image.width, self.n_filters))
            )
        preds = np.reshape(preds, (depth, image.height, image.width))
        return preds
    

    def fit_and_predict(self, image: Image, markers: MarkerContainer) -> Image:
        features = self.apply_filters(image)
        self.fit(image, markers, features=features)
        segmented_img = self.predict(image, features=features)
        return Image(data=segmented_img)


    def apply_filters(self, image: Image) -> np.ndarray:
        if self.informing: print('Appplying filters...')
        return np.transpose([filter.make_mask(image) for filter in self.__filters], (1, 2, 3, 0))


    def feature_weights(self) -> np.array:
        if 'feature_importances_' in dir(self.model):
            return {key: value for key,value in zip(self.filters_names, self.model.feature_importances_)}
        elif 'coef_' in dir(self.model):
            return self.model.coef_

    @property
    def n_filters(self) -> int:
        return len(self.__filters)  
    
def get_filters_names(filters: list[BaseFilter2D]) -> list:
    return [filter.name for filter in filters]
