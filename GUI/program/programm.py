from backend import Image

class Programm:
    __image: Image
    def __init__(self):
        pass


    def load_image(self, path_to_img: str = r'C:\Users\maxxx\VSprojects\labeling\cat.png'):
        self.__image = Image(path_to_img)


    @property
    def image(self):
        return self.__image.data
    