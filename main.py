from image.image import Image
from image.markers import Marker, MarkerContainer
import numpy as np
import matplotlib.pyplot as plt
import filters.filters_2dim as filters_2d
from segmentation.segmentation import SKSegmentation

def test_filters(path_to_image: str = 'data/1.png', show_hist: bool = False):
    image = Image(path_to_image=path_to_image, dim=2)
    if show_hist: image.histogram()
    #image.apply_filter(lambda x: x > 83) 83 80 60
    image.apply_filter(filters_2d.threshold, threshold=83)
    image.apply_filter(filters_2d.MaxFilter, size=3, times=1)
    print(image.data.shape)
    image.show()
    image.show_segments(Marker([480, 1595, 581, 1677], 1))


def test_segmentation(path_to_image: str = 'data/1.png'):
    image = Image(path_to_image=path_to_image, dim=2)
    sgm = SKSegmentation(image)
    image.show()
    image.show_segmentation()


def test_markers(path_to_image: str = 'data/1.png'):
    image = Image(path_to_image=path_to_image, dim=2)
    #t = Marker([480, 1595, 581, 1677], 1)
    markers = MarkerContainer()
    markers.from_file('data/markers.txt')
    image.draw_marker(markers)
    for el in markers.markers:
        print(el)
    image.show()


if __name__ == "__main__":
    test_filters(path_to_image='data/1.png')

