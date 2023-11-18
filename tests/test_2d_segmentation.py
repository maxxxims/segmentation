import pytest
from pytest import fixture
from backend import Image, Marker, MarkerMakerRectangle2DBinary, Segmentation
import backend.filters.filters_2dim as filters_2d
from sklearn.linear_model import LogisticRegression


path_to_test_image      = r"C:\Users\maxxx\VSprojects\back\0\0\01. Reconstructed\00. Original\im_00001.png"
path_to_test_image_bad  = r'C:\Users\maxxx\VSprojects\back\0\0\01. Reconstructed\02. Angular Decimation\02. x4\im_00001.png'
path_to_segmented_image = r"C:\Users\maxxx\VSprojects\back\0\0\02. Segmented\00. Original\im_00001.png"
path_to_border_img      = r"C:\Users\maxxx\VSprojects\back\0\0\border\border00001.png"


@fixture(scope='session')
def load_img():
    img = Image(path_to_image=path_to_test_image)
    TestSegmentation.image = img


@fixture(scope='session')
def markers():
    point1 = (1957,       2106)
    point2 = (1957 + 1000, 2106 + 1000)
    return MarkerMakerRectangle2DBinary(path_to_segmented_image, *point1, *point2).get_markers()


@fixture(scope='session')
def filters() -> list:
    filters = [filters_2d.MedianFilter(size=5), filters_2d.GaussianFilter(15), filters_2d.LaplacianDifference(),
                              filters_2d.BaseFilter2D()]
    return filters

@pytest.mark.usefixtures('load_img')
class TestSegmentation:
    image: Image
    def test_load_image(self):
        assert len(self.image.shape) == 2

    # @pytest.mark.parametrize(
    #         'point1, point2',
    #         [
    #             ((1957,        2106), ),
    #             ((1957 + 1000, 2106 + 1000), )
    #         ]
    #         )
    def test_init_markers(self, markers):
        assert len(markers) == 2
        

    def test_fit_and_predict(self, markers, filters):
        self.sgm = Segmentation(model=LogisticRegression(), filters=filters, informing=True)

        segmentated_img = self.sgm.fit_and_predict(self.image, markers)
        assert segmentated_img.height == self.image.height
        assert segmentated_img.width == self.image.width
        segmentated_img.show()
        