from image.image import Image
from image.markers import Marker, MarkerContainer
import numpy as np
import matplotlib.pyplot as plt
import filters.filters_2dim as filters_2d
from segmentation.segmentation import SKSegmentation
from segmentation.segmentation_per_pixels.segmentation2d import Segmentation
from sklearn.linear_model import LogisticRegression


def test_filters(path_to_image: str, show_hist: bool = False):
    image = Image(path_to_image=path_to_image, dim=2)
    print(image.shape())
    if show_hist: image.histogram()
    #image.apply_filter(filters_2d.Threshold(80), filters_2d.MaxFilter(3))
    image2 = Image(data = filters_2d.Threshold(80).make_mask(image))
    image2.show()
    


def test_segmentation_sk(path_to_image: str):
    image = Image(path_to_image=path_to_image, dim=2)
    sgm = SKSegmentation(image)
    image.show()
    image.show_segments(Marker([480, 1595, 581, 1677], 1))


def test_segmentation(path_to_image: str):
    # simple img
    # image = Image(data = np.array([[10 * i for i in range(10)] for j in range(5)]))
    # m = MarkerContainer([Marker([2, 3, 2, 3], 1)])
    # image.draw_marker(m)
    # image.show()
    # sgm = Segmentation(1, image, m, [filters_2d.BaseFilter2D()])

    # usual img
    image = Image(path_to_image=path_to_image, dim=2)
    m = MarkerContainer([Marker([480, 1610, 581, 1677], 1), Marker([167, 1385, 235, 1449], 0)])
    #image.apply_filter(filters_2d.Threshold(80), filters_2d.MaxFilter(3))
    image.show()
    sgm = Segmentation(LogisticRegression())
    sgm.segmentate(image, m, [filters_2d.BaseFilter2D(), filters_2d.Threshold(80)])
    image.show_segments(m[0], fill_color=0)
    image.show_segments(m[1])


def test_markers(path_to_image: str):
    image = Image(path_to_image=path_to_image, dim=2)
    markers = MarkerContainer()
    markers.from_file('data/markers.txt')
    image.draw_marker(markers)
    for marker in markers:
        print(marker)
    image.show()


if __name__ == "__main__":
    test_segmentation(path_to_image='data/1.png')

