import numpy as np
from ..image import Image, Marker, MarkerContainer, MarkerBorder2D
from .base_metric import BaseMetric

class Evaluator:
    """
        reduce border and train part from image and calculate metric
    """
    @classmethod
    def evaluate(cls, segmentated_image: Image, annotated_image: Image,
                 train_markers: MarkerContainer, border_marker: MarkerBorder2D,
                 *metrics: BaseMetric) -> float:
        EXTRA_VALUE = 128
        mask = np.copy(segmentated_image.data)
        for marker in train_markers:
            x_indexes, y_indexes = marker.get_indexes()
            segmentated_image.data[y_indexes, x_indexes] = EXTRA_VALUE
            mask[y_indexes, x_indexes] = EXTRA_VALUE

        x_indexes, y_indexes = border_marker.get_indexes()
        segmentated_image.data[y_indexes, x_indexes] = EXTRA_VALUE
        mask[y_indexes, x_indexes] = EXTRA_VALUE

        y_index_test, x_index_test  = np.where(mask != EXTRA_VALUE) # TRUE
        # segmentated_image.data[y_index_test, x_index_test] = 255
        res = segmentated_image.data[y_index_test, x_index_test]
        
        y_real = np.copy(annotated_image.data[y_index_test, x_index_test])
        y_pred = mask[y_index_test, x_index_test]

        if np.max(y_pred) == 1:
            #print(f'upscale y_pred to 0-255')
            y_pred *= 255

        logs = {}
        for metric in metrics:
            metric_value = metric.get_score(y_real=y_real, y_pred=y_pred)
            logs[metric.name] = metric_value
            # print(f'{metric.name} = {metric_value}')
        return logs
        # segmentated_image.show(show_original=False, title='Image for evaluate metrics')
        