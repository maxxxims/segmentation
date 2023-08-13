import numpy as np
from image.image import Image
from image.markers import Marker, MarkerContainer
from filters.filters import BaseFilter2D
import pandas as pd



class Segmentation:
    def __init__(self, model, image: Image, markers: MarkerContainer, filters: list[BaseFilter2D]) -> None:
        self.model = model
        self.height, self.widht = image.shape()
        self.n_filters = len(filters)
        # переводим в массив [[кол-во фильтров] * высота * ширина (=количество пикселей)]
        filtred_data = np.reshape(np.transpose(np.array([ filter.make_mask(image) for filter in filters])), 
                                       (self.height * self.widht, self.n_filters))
        
        #print(self.filtred_data)
        print(filtred_data.shape)
        print(2 * self.height + 3  )

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
        model.fit(x_test, y_test)
        self.model = model
        y_pred = model.predict(filtred_data)
        self.pred_img = np.transpose(np.reshape(y_pred, (self.widht, self.height)))