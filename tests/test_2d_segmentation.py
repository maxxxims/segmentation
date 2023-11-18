import pytest
from backend import Image, Marker, MarkerMakerRectangle2DBinary, Segmentation
import backend.filters.filters_2dim as filters_2d
from sklearn.linear_model import LogisticRegression


class TestSegmentation:
    path_to_test_image      = r"C:\Users\maxxx\VSprojects\back\0\0\01. Reconstructed\00. Original\im_00001.png"
    path_to_test_image_bad  = r'C:\Users\maxxx\VSprojects\back\0\0\01. Reconstructed\02. Angular Decimation\02. x4\im_00001.png'
    path_to_segmented_image = r"C:\Users\maxxx\VSprojects\back\0\0\02. Segmented\00. Original\im_00001.png"
    path_to_border_img      = r"C:\Users\maxxx\VSprojects\back\0\0\border\border00001.png"

    def test_load_image(self):
        print('IMG WORKING')
        self.image = Image(path_to_image=self.path_to_test_image)
        assert len(self.image.shape) == 2

    # @pytest.mark.parametrize(
    #         'point1, point2',
    #         [
    #             ((1957,        2106), ),
    #             ((1957 + 1000, 2106 + 1000), )
    #         ]
    #         )
    def test_init_markers(self):
        point1 = (1957, 2106)
        point2 = (1957 + 1000, 2106 + 1000)
        self.markers = MarkerMakerRectangle2DBinary(self.path_to_segmented_image, *point1, *point2).get_markers()
        assert len(self.markers) == 2


    def test_init_filters(self):
        self.filters = [filters_2d.MedianFilter(size=5), filters_2d.GaussianFilter(15), filters_2d.LaplacianDifference(),
                              filters_2d.BaseFilter2D()]
        


    def test_init_segmentation(self):
        self.test_init_filters()
        self.sgm = Segmentation(model=LogisticRegression(), filters=self.filters, informing=True)

    
    def test_fit_and_predict(self):
        self.test_load_image()
        self.test_init_markers()
        self.test_init_segmentation()
        self.segmentated_img = self.sgm.fit_and_predict(self.image, self.markers)
        assert self.segmentated_img.height == self.image.height
        assert self.segmentated_img.width == self.image.width