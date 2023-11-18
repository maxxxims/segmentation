import pytest
from backend import Image, Marker, MarkerMakerRectangle2DBinary, Image3D, \
    MarkerMaker3DBinary
from sklearn.linear_model import LogisticRegression
from directory import Directory 


class TestMarkerMaker:
    img_folder = Directory(main_path='C:/Users/maxxx/VSprojects/back/0/0')

    def test_load_3d_image(self):
        self.img_3d = Image3D(img_pathes = self.img_folder.orign_folder)
        self.img_3d_annotated = Image3D(img_pathes = self.img_folder.segmented_folder)
        # print(self.img_folder.orign_folder)
        # print(f'shape = {self.img_3d.shape}')
        assert len(self.img_3d.shape) == 3
        

    def test_init_marker_maker3D(self):
        self.test_load_3d_image()
        point1 = (1957,       2106,       0)
        point2 = (1957 + 100, 2106 + 500, 0 + 4)
        self.markers = MarkerMaker3DBinary(*point1, *point2).get_markers(self.img_3d_annotated)


    def test_fill_markers(self):
        self.test_init_marker_maker3D()
        assert len(self.markers) == 2
        
        self.img_3d.clear_cache()
        # self.load_images(np.min(marker.z_index), marker.z8)
        self.img_3d.load_images(0, 10)

        for marker in self.markers:
            print(marker.z_indexes)
            self.img_3d.draw_marker(marker, color=marker.value * 255)

        for i in range(0, 5):
            self.img_3d.show(i)
