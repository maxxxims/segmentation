import skimage.filters as skfilters
from image.image import Image
import matplotlib.pyplot as plt


class SKSegmentation:
    def __init__(self, image: Image):
        test = skfilters.threshold_local(image.data, block_size=101, offset=10) 
        image.data = (image.data > test)

        #