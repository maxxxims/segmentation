import numpy as np
from image.image import Image
from image import Marker, MarkerContainer
from filters.filters import BaseFilter2D
import pandas as pd


class Segmentation:
    def __init__(self, model) -> None:
        self.model = model

    
    def segmentate(self, image: Image, markers: MarkerContainer,
                filters: list[BaseFilter2D], inplace_image: bool = True, informing: bool = True, test_markers=False):
        self.dim = image.dim
        self.height, self.widht = image.shape()
        self.n_filters = len(filters)

        if informing: print('Appplying filters...')
        filtred_data = get_selection_2d(image, filters, self.height, self.widht, self.n_filters)
        self.filters_names = get_filters_names(filters)


        if informing: print('Making test data...')
        x_test, y_test = get_test_data_2d(filtred_data, markers, self.height)
        if test_markers:
            print(np.shape(x_test), np.shape(filtred_data))
            test_markers_(markers, filtred_data, self.height, self.widht)
            return None

        # обучение модели
        if informing: print('Fitting model...')
        self.model.fit(x_test, y_test)
        self.model = self.model

        if informing: print('Making predictions...')
        y_pred = self.model.predict(filtred_data)
        if informing: print('Transforming result...')
        self.pred_img = reshape_data(y_pred, self.height, self.widht)
        if inplace_image:
            image.data = self.pred_img 
        else:
            return self.pred_img 
        

    def feature_weights(self) -> np.array:
        if 'feature_importances_' in dir(self.model):
            return {key: value for key,value in zip(self.filters_names, self.model.feature_importances_)}
        elif 'coef_' in dir(self.model):
            return self.model.coef_
        

def get_selection_2d(image: Image, filters: list[BaseFilter2D],
                    height: int, widht: int, n_filters: int) -> np.array:
    # переводим в массив [[кол-во фильтров] * высота * ширина (=количество пикселей)]
    return np.reshape(np.transpose(np.array([ filter.make_mask(image) for filter in filters])), 
                                        (height * widht, n_filters))
    
def get_filters_names(filters: list[BaseFilter2D]) -> list:
    return [filter.name for filter in filters]


def get_test_data_2d(filtred_data: np.array, markers: MarkerContainer, height: int) -> tuple[list, list]:
    # делаем тестовую выборку на основе разметки
    # x_test = []
    # y_test = []
    # for marker in markers:
    #     if marker.type == 'rectangle':
    #         for x in range(marker.x1, marker.x4 + 1):                       # +1 ?
    #             for y in range(marker.y1, marker.y4 + 1):
    #                 x_test.append(filtred_data[x * height + y])
    #                 y_test.append(marker.value)
        
    #     elif marker.type == 'fill':
    #         for x, y in marker.points:
    #             x_test.append(filtred_data[x * height + y])
    #             y_test.append(marker.value)
    x_test = []
    y_test = []
    for marker in markers:
        x_indexes = marker.to_x_selection_index(height)
        for x in x_indexes:
            x_test.append(filtred_data[x])
            y_test.append(marker.value)

    return (x_test, y_test)


def reshape_data(y_pred: np.array, height: int, widht: int) -> np.array:
    return np.transpose(np.reshape(y_pred, (widht, height)))


def test_markers_(markers: MarkerContainer, filtred_data: np.array, height: int, widht: int, filter_index: int = -1):
    x_test = []
    x_indexes = []
    for marker in markers:
        x_indexes += marker.to_x_selection_index(height)
    for i in range(len(filtred_data)):
        if i in x_indexes:
            x_test.append(0)
        else:
            x_test.append(filtred_data[i,-1])
    print('done')
    img = Image(data=reshape_data(x_test, height, widht))
    img.show()
