from typing import Any
from ..image import Image
import numpy as np


class BaseMetric:
    @classmethod
    def make_mask(cls, segmentated_image: Image, annotated_image: Image,
                  *args: Any, **kwds: Any) -> np.ndarray:
        return segmentated_image.data == annotated_image.data

    @classmethod
    def get_score(cls, *, y_real: np.ndarray, y_pred: np.ndarray) -> float:...
        

    @classmethod
    def __call__(cls, segmentated_image: Image, annotated_image: Image,
                 *args: Any, **kwds: Any) -> float:
        return cls.get_score(segmentated_image, annotated_image,
                 *args, **kwds)