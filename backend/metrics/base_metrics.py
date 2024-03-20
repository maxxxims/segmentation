from typing import Any
from ..image import Image
import numpy as np
from sklearn.metrics import f1_score



class BaseMetric:
    name = 'BaseMetric'
    @classmethod
    def get_score(cls, *, y_real: np.ndarray, y_pred: np.ndarray) -> float: ...



class Accuracy(BaseMetric):
    name = 'Accuracy'
    @classmethod
    def get_score(cls, *, y_real: np.ndarray, y_pred: np.ndarray) -> float:
        return np.sum(y_real == y_pred) / len(y_real)
    


class F1_binary(BaseMetric):
    name = 'F1 binary'
    @classmethod
    def get_score(cls, *, y_real: np.ndarray, y_pred: np.ndarray) -> float:
        return f1_score(y_true=y_real, y_pred=y_pred)
    



def calc_porosity(y_arr: np.ndarray) -> float:
    return np.sum(y_arr == 0) / len(y_arr)
    

class EPorosity(BaseMetric):
    name = 'Porosity relative difference'
    @classmethod
    def get_score(cls, *, y_real: np.ndarray, y_pred: np.ndarray) -> float:
        porosity_real = calc_porosity(y_real)
        porosity_pred = calc_porosity(y_pred)
        return 100 * np.abs(porosity_real - porosity_pred) / porosity_real
    


class IoU_pores(BaseMetric):
    name = 'IoU_pores'
    @classmethod
    def get_score(cls, *, y_real: np.ndarray, y_pred: np.ndarray) -> float:
        intersection = np.sum((y_real == 0) & (y_pred == 0)) #np.sum(y_real * y_pred) 
        union = np.sum(y_real == 0) + np.sum(y_pred == 0) - intersection
        return intersection / union
    
