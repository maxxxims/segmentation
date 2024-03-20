import numpy as np
from ..image import Image, Marker, MarkerContainer, MarkerBorder2D
from .base_metrics import BaseMetric
from ..filters import filters_2dim as filters_2d


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
            #segmentated_image.data[y_indexes, x_indexes] = EXTRA_VALUE
            mask[y_indexes, x_indexes] = EXTRA_VALUE

        if border_marker is not None:
            x_indexes, y_indexes = border_marker.get_indexes()
            #segmentated_image.data[y_indexes, x_indexes] = EXTRA_VALUE
            mask[y_indexes, x_indexes] = EXTRA_VALUE

        y_index_test, x_index_test  = np.where(mask != EXTRA_VALUE) # TRUE
        # segmentated_image.data[y_index_test, x_index_test] = 255
        #res = segmentated_image.data[y_index_test, x_index_test]
        
        y_real = np.copy(annotated_image.data[y_index_test, x_index_test])
        y_pred = mask[y_index_test, x_index_test]

        y_real[y_real > 0] = 1
        

        # print(np.unique(y_real), np.unique(y_pred))

        # if np.max(y_pred) == 1:
        #     #print(f'upscale y_pred to 0-255')
        #     y_pred *= 255

        logs = {}
        for metric in metrics:
            metric_value = metric.get_score(y_real=y_real, y_pred=y_pred)
            logs[metric.name] = metric_value
            # print(f'{metric.name} = {metric_value}')
        return logs
        # segmentated_image.show(show_original=False, title='Image for evaluate metrics')



class EvaluatorBorder:
    @classmethod
    def evaluate(cls, N: int, segmentated_image: Image, annotated_image: Image,
                 train_markers: MarkerContainer, border_marker: MarkerBorder2D,
                 *metrics: BaseMetric) -> float:
        """
            annotated - gt
        """
        EXTRA_VALUE = 128
        mask_border_area = filters_2d.Dilation(size=N).make_mask(annotated_image) - filters_2d.Erosion(size=N).make_mask(annotated_image)
        mask = np.copy(segmentated_image.data)
        mask[mask_border_area != 255] = EXTRA_VALUE
        for marker in train_markers:
            x_indexes, y_indexes = marker.get_indexes()
            mask[y_indexes, x_indexes] = EXTRA_VALUE

        if border_marker is not None:
            x_indexes, y_indexes = border_marker.get_indexes()
            mask[y_indexes, x_indexes] = EXTRA_VALUE

        y_index_test, x_index_test  = np.where(mask != EXTRA_VALUE) # TRUE
        # segmentated_image.data[y_index_test, x_index_test] = 255
        #res = segmentated_image.data[y_index_test, x_index_test]
        
        y_real = np.copy(annotated_image.data[y_index_test, x_index_test])
        y_pred = mask[y_index_test, x_index_test]

        y_real[y_real > 0] = 1
        

        print(np.unique(y_real), np.unique(y_pred))

        # if np.max(y_pred) == 1:
        #     #print(f'upscale y_pred to 0-255')
        #     y_pred *= 255

        logs = {}
        for metric in metrics:
            metric_value = metric.get_score(y_real=y_real, y_pred=y_pred)
            logs[metric.name] = metric_value
            # print(f'{metric.name} = {metric_value}')
        return logs


class Evaluator3D:
    """
        reduce border and train part from image and calculate metric
    """
    @classmethod
    def evaluate(cls, segmentated_image: np.ndarray, annotated_image: np.ndarray,
                 train_markers: MarkerContainer, border_marker: MarkerBorder2D,
                 *metrics: BaseMetric) -> float:
        EXTRA_VALUE = 999
        mask = np.copy(segmentated_image)
        for marker in train_markers:
            x_indexes, y_indexes, z_indexes = marker.get_indexes()
            mask[z_indexes, y_indexes, x_indexes] = EXTRA_VALUE

        x_indexes, y_indexes = border_marker.get_indexes()
        mask[:, y_indexes, x_indexes] = EXTRA_VALUE

        z_indexes, y_index_test, x_index_test  = np.where(mask != EXTRA_VALUE) # TRUE
        
        y_real = np.copy(annotated_image[z_indexes, y_index_test, x_index_test])
        y_pred = mask[z_indexes, y_index_test, x_index_test]

        if np.max(y_pred) == 1:
            #print(f'upscale y_pred to 0-255')
            y_pred *= 255

        logs = {}
        for metric in metrics:
            metric_value = metric.get_score(y_real=y_real, y_pred=y_pred)
            logs[metric.name] = metric_value
        return logs