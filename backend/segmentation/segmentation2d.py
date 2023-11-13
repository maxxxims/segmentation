import numpy as np
from ..image import Image, Marker, MarkerContainer
from ..filters.filters import BaseFilter2D
import pandas as pd
from sklearn.utils import shuffle


class Segmentation:
    def __init__(self, model, image: Image, filters: list[BaseFilter2D], informing: bool = True) -> None:
        self.informing = informing
        self.model = model
        self.image = image
        self.filters   = filters
        self.n_filters = len(filters)
        self.height, self.widht = self.image.shape()
        if self.informing: print('Appplying filters...')
        self.features = np.transpose([filter.make_mask(image) for filter in filters], (1, 2, 0))
        self.filters_names = get_filters_names(filters)
        


    def fit(self, markers: MarkerContainer, check: bool = False):
        if self.informing: print('Making test data...')
        # get x_train and y_train
        class2data = {}
        y_train = []
        for m in markers:
            value = m.value
            x_indexes, y_indexes = m.get_indexes()
            #print(f'res = {res}, {res[0].shape}, {res[1].shape}')
            class2data[value] = self.features[y_indexes, x_indexes]
            y_train += [value] * len(x_indexes)
        
        #print(f'y values = {np.unique(y_train)}')
        x_train = np.concatenate([class2data[m.value] for m in markers])
        x_train, y_train = shuffle(x_train, y_train, random_state=42)

        if self.informing: print('Fitting model...')
        self.model.fit(x_train, y_train)

        print(f'x_train shape = {np.shape(x_train)}, y_train shape = {np.shape(y_train)}')
        if check:
            from matplotlib import pyplot as plt
            new_data = self.image.data
            for m in markers:
                value = m.value
                x_indexes, y_indexes = m.get_indexes()
                new_data[y_indexes, x_indexes] = value * 255
            plt.imshow(new_data, cmap='gray')
            plt.show()

    def predict(self) -> Image:
        preds = self.model.predict(self.features.reshape((self.height * self.widht, self.n_filters)))
        # print(f'preds shape = {preds.shape}')
        preds = np.reshape(preds, (self.height, self.widht))
        # print(f'new preds shape = {preds.shape}')
        return Image(data=preds)
        

    def feature_weights(self) -> np.array:
        if 'feature_importances_' in dir(self.model):
            return {key: value for key,value in zip(self.filters_names, self.model.feature_importances_)}
        elif 'coef_' in dir(self.model):
            return self.model.coef_
        
    
def get_filters_names(filters: list[BaseFilter2D]) -> list:
    return [filter.name for filter in filters]
