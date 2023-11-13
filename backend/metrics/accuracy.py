from typing import Any
import numpy as np
from backend.image import Image
from .base_metric import BaseMetric
from ..image import Image
import matplotlib.pyplot as plt


class Accuracy(BaseMetric):
    name = 'Accuracy'
    @classmethod
    def get_score(cls, *, y_real: np.ndarray, y_pred: np.ndarray) -> float:
        return np.sum(y_real == y_pred) / len(y_real)

    @classmethod
    def show_diffrence(cls, segmentated_image: Image, 
                  annotated_image: Image, *args: Any, **kwds: Any) -> np.ndarray:
        #plt.imshow(segmentated_image.data - annotated_image.data)
        plt.imshow(cls.make_mask(segmentated_image, annotated_image), cmap='gray')
        plt.show()