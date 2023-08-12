from image.image import Image
import numpy as np
import matplotlib.pyplot as plt
import filters.filters as filters

def test_image():
    image = Image(path_to_image='data/1.png', dim=2)
    #image.histogram()
    #image.apply_filter(lambda x: x > 83) 
    image.apply_filter(filters.threshold, threshold=83)
    image.apply_filter(filters.MaxFilter, size=3, times=1)
    print(image.data.shape)
    image.show()


if __name__ == "__main__":
    test_image()