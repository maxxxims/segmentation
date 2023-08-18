import numpy as np
from image.image import Image
from image.markers import Marker, MarkerContainer
from filters.filters import BaseFilter2D
import pandas as pd


class Segmentation:
    def __init__(self, model) -> None:
        self.model = model

    
    def segmentate(self, image: Image, markers: MarkerContainer,
                filters: list[BaseFilter2D], inplace_image: bool = True):
        self.height, self.widht = image.shape()
        self.n_filters = len(filters)
        # переводим в массив [[кол-во фильтров] * высота * ширина (=количество пикселей)]
        filtred_data = np.reshape(np.transpose(np.array([ filter.make_mask(image) for filter in filters])), 
                                       (self.height * self.widht, self.n_filters))
        self.filters_names = [filter.name for filter in filters]
        #print(self.filtred_data)
        #print(filtred_data.shape)
        #print(2 * self.height + 3  )

        # делаем тестовую выборку на основе разметки
        x_test = []
        y_test = []
        for marker in markers:
            for x in range(marker.x1, marker.x4 + 1):                       # +1 ?
                for y in range(marker.y1, marker.y4 + 1):
                    x_test.append(filtred_data[x * self.height + y])
                    y_test.append(marker.value)
        #print(x_test)

        # обучение модели
        self.model.fit(x_test, y_test)
        self.model = self.model
        y_pred = self.model.predict(filtred_data)
        #print(y_pred)
        self.pred_img = np.transpose(np.reshape(y_pred, (self.widht, self.height)))
        if inplace_image:
            image.data = self.pred_img 
        else:
            return self.pred_img 
        

    def feature_weights(self) -> np.array:
        if 'feature_importances_' in dir(self.model):
            return {key: value for key,value in zip(self.filters_names, self.model.feature_importances_)}
        elif 'coef_' in dir(self.model):
            return self.model.coef_