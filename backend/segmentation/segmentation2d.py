import numpy as np
from ..image import Image, Marker, MarkerContainer
from ..filters.filters import BaseFilter2D
import pandas as pd
from sklearn.utils import shuffle
# from tqdm.notebook import tqdm
from tqdm import tqdm

class Segmentation:
    def __init__(self, model, filters: list[BaseFilter2D], informing: bool = True) -> None:
        self.informing = informing
        self.__model = model
        self.__filters   = np.copy(filters)
        self.__filters_names = get_filters_names(filters)
        

    def fit(self, image: Image, markers: MarkerContainer, 
            check: bool = False, features: np.ndarray = None):
        if features is None:
            features = self.apply_filters(image)
        if self.informing: print('Making train data...')
        # get x_train and y_train
        class2data = {}
        y_train = []
        for m in markers:
            value = m.value
            x_indexes, y_indexes = m.get_indexes()
            class2data[value] = features[y_indexes, x_indexes]
            # print(f'feature shape = {np.shape(features[y_indexes, x_indexes])}')
            y_train += [value] * len(x_indexes)
        
        #print(f'y values = {np.unique(y_train)}')
        x_train = np.concatenate([class2data[m.value] for m in markers])
        # print(f'x_train shape = {np.shape(x_train)}, y_train shape = {np.shape(y_train)}')
        x_train, y_train = shuffle(x_train, y_train, random_state=42)
        
        if self.informing: print('Fitting model...')
        self.__model.fit(x_train, y_train)
        if self.informing:
            print(f'x_train shape = {np.shape(x_train)}, y_train shape = {np.shape(y_train)}')
        # if check:
        #     from matplotlib import pyplot as plt
        #     new_data = self.image.data
        #     for m in markers:
        #         value = m.value
        #         x_indexes, y_indexes = m.get_indexes()
        #         new_data[y_indexes, x_indexes] = value * 255
        #     plt.imshow(new_data, cmap='gray')
        #     plt.show()


    def predict(self, image: Image, features: np.ndarray = None) -> Image:
        """
            Segmentate image
        """
        if features is None:
            features = self.apply_filters(image)
        if self.informing: print('Making predictions...')
        preds = self.__model.predict(features.reshape((image.height * image.width, self.n_filters)))
        preds = np.reshape(preds, (image.height, image.width))
        return Image(data=preds)
    

    def fit_and_predict(self, image: Image, markers: MarkerContainer) -> Image:
        features = self.apply_filters(image)
        self.fit(image, markers, features=features)
        segmented_img = self.predict(image, features=features)
        return segmented_img


    def apply_filters(self, image: Image) -> np.ndarray:
        if self.informing: 
            print('Appplying filters...')
            return np.transpose([filter.make_mask(image) for filter in tqdm(self.__filters)], (1, 2, 0))
        else:
            return np.transpose([filter.make_mask(image) for filter in self.__filters], (1, 2, 0))

    def feature_weights(self) -> np.array:
        if 'feature_importances_' in dir(self.__model):
            return {key: value for key,value in zip(self.__filters_names, self.__model.feature_importances_)}
        elif 'coef_' in dir(self.__model):
            return {f'{self.__filters_names[i]}': self.__model.coef_[0][i] for i in range(len(self.__filters))}
            # return self.__model.coef_
    @property
    def n_filters(self) -> int:
        return len(self.__filters)  
    
def get_filters_names(filters: list[BaseFilter2D]) -> list:
    return [filter.name for filter in filters]
