from directory import Directory
from backend import Image3D


DATA_PATH = r'C:\Users\maxxx\VSprojects\back\0\0'


def test_3d_img():
    folder = Directory(main_path=DATA_PATH)
    print(folder.orign_folder)
    img = Image3D(img_pathes=folder.orign_folder, batch_size=10)
    img[0].show()
    img.load_batch(batch_number=1)
    img[15].show()



if __name__ == '__main__':
    test_3d_img()
