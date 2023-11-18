import pytest
from pytest import fixture
from backend import Image, Marker, MarkerMakerRectangle2DBinary, Image3D, \
    MarkerMaker3DBinary, BaseFilter2D, Segmentation3D
from sklearn.linear_model import LogisticRegression
from directory import Directory 
import numpy as np
from matplotlib import pyplot as plt

@fixture(scope="session")
def load_images() -> tuple[Image3D, Image3D]:
    img_folder = Directory(main_path='C:/Users/maxxx/VSprojects/back/0/0')
    img_3d = Image3D(img_pathes = img_folder.orign_folder)
    img_3d_annotated = Image3D(img_pathes = img_folder.segmented_folder)
    TestMarkerMaker.img_3d = img_3d
    TestMarkerMaker.img_3d_annotated = img_3d_annotated


@fixture(scope="session")
def markers():
    point1 = (1957,       2106,       0)
    point2 = (1957 + 100, 2106 + 500, 0 + 4)
    return MarkerMaker3DBinary(*point1, *point2).get_markers(TestMarkerMaker.img_3d_annotated)


@pytest.mark.usefixtures('load_images')
class TestMarkerMaker:
    img_3d:           Image3D
    img_3d_annotated: Image3D
    def test_load_3d_image(self):
        assert self.img_3d.shape == self.img_3d_annotated.shape
        assert len(self.img_3d.shape) == 3
        

    def test_init_marker_maker3D(self, markers):
        assert len(markers) == 2
        for _ in range(2):
            x_indexes, y_indexes, z_indexes = markers[0].get_indexes()
            assert len(x_indexes) == len(y_indexes) == len(z_indexes)


    def test_fill_markers(self, markers):
        self.img_3d.clear_cache()
        # self.img_3d.load_images(np.min(marker.z_indexes), marker.z8)
        self.img_3d.load_images(0, 10)
        for marker in markers:
            self.img_3d.draw_marker(marker, color=marker.value * 255)
        for i in range(0, 5):
            self.img_3d.show(i)


    def test_3d_filters(self):
        n_filters = 4
        n_imgs = 5
        self.img_3d.clear_cache()
        self.img_3d.load_images(0, n_imgs - 1)
        filter = BaseFilter2D()
        
        features = np.array([
            filter.make_mask(self.img_3d) for _ in range(n_filters)
            ])
        print(f'features shape = {features.shape}')


        assert (features == self.img_3d.data).all()
        self.img_3d.show(0)


class TestSegmentation3D(TestMarkerMaker):
    def test_fit_function(self, markers):
        sgm = Segmentation3D(LogisticRegression(),
                            [BaseFilter2D(), BaseFilter2D()],
                            batch_size=10, informing=True)
        sgm.fit(self.img_3d, markers)

        self.img_3d.clear_cache()
        self.img_3d.load_images(0, 2)
        preds = sgm.predict(self.img_3d)

        assert preds.shape == (3, self.img_3d.height, self.img_3d.width)

        for i in range(0, 3):
            Image(data=preds[i]).show()