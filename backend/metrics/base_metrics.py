from typing import Any
from ..image import Image
import numpy as np


class BaseMetric:
    name = 'BaseMetric'
    @classmethod
    def get_score(cls, *, y_real: np.ndarray, y_pred: np.ndarray) -> float: ...



class Accuracy(BaseMetric):
    name = 'Accuracy'
    @classmethod
    def get_score(cls, *, y_real: np.ndarray, y_pred: np.ndarray) -> float:
        return np.sum(y_real == y_pred) / len(y_real)