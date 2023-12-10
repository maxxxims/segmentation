import pytest
from pytest import fixture
from backend import Image, Marker, MarkerMakerRectangle2DBinary, Image3D, \
    MarkerMaker3DBinary, BaseFilter2D, Segmentation3D, BaseFilter3D
import backend.filters.filters_3dim as filters_3d
from sklearn.linear_model import LogisticRegression
from directory import Directory 
import numpy as np
from matplotlib import pyplot as plt

@pytest.mark.usefixtures('load_images')
class TestMarkerMaker:
    img_3d:           Image3D
    img_3d_annotated: Image3D
    def test_load_3d_image(self):
        assert self.img_3d.shape == self.img_3d_annotated.shape
        assert len(self.img_3d.shape) == 3
        

    def test_init_marker_maker3D(self, markers3d):
        assert len(markers3d) == 2
        for _ in range(2):
            x_indexes, y_indexes, z_indexes = markers3d[0].get_indexes()
            assert len(x_indexes) == len(y_indexes) == len(z_indexes)


    def test_fill_markers(self, markers3d):
        self.img_3d.clear_cache()
        # self.img_3d.load_images(np.min(marker.z_indexes), marker.z8)
        self.img_3d.load_images(0, 10)
        for marker in markers3d:
            self.img_3d.draw_marker(marker, color=marker.value * 255)
        for i in range(0, 5):
            self.img_3d.show(i)


    def test_3d_base_filters(self):
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


    def test_3d_filters(self):
        """
            apply filters and show
        """
        n_imgs = 15
        self.img_3d.clear_cache()
        self.img_3d.load_images(0, n_imgs - 1)
        filter = filters_3d.GaussianFilter(10)
        
        features = filter.make_mask(self.img_3d)

        print(f'features shape = {features.shape}')

        for i in range(3):
            Image(data=features[i]).show(title='Gaussian 3D Filter')


class TestSegmentation3D(TestMarkerMaker):
    def test_fit_function(self, markers3d):
        sgm = Segmentation3D(LogisticRegression(),
                            [BaseFilter3D(), BaseFilter3D()],
                            batch_size=10, informing=True)
        sgm.fit(self.img_3d, markers3d)

        self.img_3d.clear_cache()
        self.img_3d.load_images(0, 2)
        preds = sgm.predict(self.img_3d)

        assert preds.shape == (3, self.img_3d.height, self.img_3d.width)

        for i in range(0, 3):
            Image(data=preds[i]).show()