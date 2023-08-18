import numpy as np
import matplotlib.pyplot as plt
from image import Image, Marker, MarkerContainer
from segmentation import SKSegmentation, Segmentation
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import filters.filters_2dim as filters_2d


def test_filters(path_to_image: str, show_hist: bool = False):
    image = Image(path_to_image=path_to_image, dim=2)
    print(image.shape())
    if show_hist: image.histogram()
    #image.apply_filter(filters_2d.Threshold(80), filters_2d.MaxFilter(3))
    image.apply_filter(filters_2d.Threshold(80))
    image.show()
    

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
    image.show()
    sgm = Segmentation(RandomForestClassifier())
    sgm.segmentate(image, m, [filters_2d.MedianFilter(5), filters_2d.GaussianFilter(5), filters_2d.LaplacianDifference(),
                               filters_2d.BaseFilter2D()])
    image.show_segments(m[0], fill_color=0)
    image.show_segments(m[1])
    print(sgm.feature_weights())


def test_markers(path_to_image: str):
    image = Image(path_to_image=path_to_image, dim=2)
    markers = MarkerContainer()
    markers.from_file('data/markers_3.txt')
    image.draw_marker(markers)
    for marker in markers:
        print(marker)
    image.show()


def test_fill_markers(path_to_image: str):
    image = Image(path_to_image=path_to_image, dim=2)
    mkr = MarkerContainer()
    mkr.from_file('data/marker_fill_1.txt')
    image.draw_marker(mkr)
    image.show()


if __name__ == "__main__":
    test_markers(path_to_image='data/3.png')

