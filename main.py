import numpy as np
import matplotlib.pyplot as plt
from backend.image import Image, Marker, MarkerRectangle2D, MarkerFill2D, MarkerContainer
from backend.filters import  filters_2dim as filters_2d
from backend.filters.filters import BaseFilter2D
from backend.segmentation import Segmentation
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
#import .filters.filters_2dim as BaseFilter2D



def test_filters(path_to_image: str, show_hist: bool = False):
    image = Image(path_to_image=path_to_image, dim=2)
    print(image.shape())
    if show_hist: image.histogram()
    #image.apply_filter(filters_2d.Threshold(80), filters_2d.MaxFilter(3))
    image.apply_filter(filters_2d.Threshold(80))
    image.show()
    
def test_segmentation(path_to_image: str):
    # simple img
    # image = Image(data = np.array([[10 * i for i in range(10)] for j in range(5)]))
    # m = MarkerContainer([Marker([2, 3, 2, 3], 1)])
    # image.draw_marker(m)
    # image.show()
    # sgm = Segmentation(1, image, m, [filters_2d.BaseFilter2D()])
    # usual img
    image = Image(path_to_image=path_to_image, dim=2)
    m = MarkerContainer([MarkerRectangle2D([480, 1610, 581, 1677], 1), MarkerRectangle2D([167, 1385, 235, 1449], 0)])
    image.show()
    sgm = Segmentation(RandomForestClassifier())
    sgm.segmentate(image, m, [filters_2d.MedianFilter(size=5), filters_2d.GaussianFilter(5), filters_2d.LaplacianDifference(),
                               filters_2d.BaseFilter2D()], test_markers=False)
    image.show_segments(m[0], fill_color=0)
    image.show_segments(m[1])
    print(sgm.feature_weights())


def test_markers(path_to_image: str):
    image = Image(path_to_image=path_to_image, dim=2)
    markers = MarkerContainer()
    markers.from_file('data/markers_3.json')
    image.draw_marker(markers)
    for marker in markers:
        print(marker)
    image.show()


def test_fill_markers(path_to_image: str):
    image = Image(path_to_image=path_to_image, dim=2)
    mkr = MarkerContainer()
    mkr.from_file('data/markers_1_fill.json')
    image.draw_marker(mkr)
    image.show()


def test_hand_markers(path_to_file: str):
    img = Image(path_to_image='data/1.png', dim=2)
    img.show()
    markers = MarkerContainer()
    markers.from_png(path_to_file, img)
    for m in markers:
        img.draw_marker(m)
    img.show()


if __name__ == "__main__":
    test_segmentation(path_to_image='data/1.png')
    test_segmentation(path_to_image='backend/data/1.png')
    test_hand_markers(path_to_file='data/1 — копия.png')