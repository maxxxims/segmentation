
import pytest
from pytest import fixture
from backend import Image, Marker, MarkerMakerRectangle2DBinary, Segmentation
import backend.filters.filters_2dim as filters_2d
from sklearn.linear_model import LogisticRegression

from backend.image3d.image3d import Image3D
from backend.image3d.marker_maker3d import MarkerMaker3DBinary
from directory.directory import Directory
# from conftest import 

path_to_test_image      = r"C:\Users\maxxx\VSprojects\back\0\0\01. Reconstructed\00. Original\im_00001.png"
path_to_test_image_bad  = r'C:\Users\maxxx\VSprojects\back\0\0\01. Reconstructed\02. Angular Decimation\02. x4\im_00001.png'
path_to_segmented_image = r"C:\Users\maxxx\VSprojects\back\0\0\02. Segmented\00. Original\im_00001.png"
path_to_border_img      = r"C:\Users\maxxx\VSprojects\back\0\0\border\border00001.png"




@fixture(scope='function', autouse=True)
def load_img2d(request):
    img = Image(path_to_image=path_to_test_image)
    request.cls.image = img


@fixture(scope='session', autouse=True)
def markers():
    point1 = (1957,       2106)
    point2 = (1957 + 1000, 2106 + 1000)
    return MarkerMakerRectangle2DBinary(path_to_segmented_image, *point1, *point2).get_markers()


@fixture(scope='session', autouse=True)
def filters() -> list:
    filters = [filters_2d.MedianFilter(size=5), filters_2d.GaussianFilter(15), filters_2d.LaplacianDifference(),
                              filters_2d.BaseFilter2D()]
    return filters



@fixture(scope="function")
def load_images(request) -> tuple[Image3D, Image3D]:
    img_folder = Directory(main_path='C:/Users/maxxx/VSprojects/back/0/0')
    img_3d = Image3D(img_pathes = img_folder.orign_folder)
    img_3d_annotated = Image3D(img_pathes = img_folder.segmented_folder)
    request.cls.img_3d = img_3d
    request.cls.img_3d_annotated = img_3d_annotated


@fixture(scope="function")
def markers3d(request):
    point1 = (1957,       2106,       0)
    point2 = (1957 + 100, 2106 + 500, 0 + 4)
    return MarkerMaker3DBinary(*point1, *point2).get_markers(request.cls.img_3d_annotated)
