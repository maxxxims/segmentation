import os
import numpy as np


class Directory:
    ORIGIN_PATH  = '01. Reconstructed/00. Original'
    BINNING_PATH = '01. Reconstructed/01. Binning/0.2 x4'
    ANGULAR_DECIMATION_PATH = '01. Reconstructed/02. Angular Decimation/02. x4'
    SEGMENTED_PATH = '02. Segmented/00. Original'


    def __init__(self, main_path: str) -> None:
        self.main_path  = main_path
        self.orign_folder     = self.load_images(self.ORIGIN_PATH)
        self.binning_folder   = self.load_images(self.BINNING_PATH)
        self.ang_dec_folder   = self.load_images(self.ANGULAR_DECIMATION_PATH)
        self.segmented_folder = self.load_images(self.SEGMENTED_PATH)


    def load_images(self, path: str) -> list: 
        imges_names = os.listdir(os.path.join(self.main_path, path))
        # sorting ...
        return [os.path.join(self.main_path, path, name) for name in sorted(imges_names)]
    
    
if __name__ == '__main__':
    d = Directory(main_path=r'C:\Users\maxxx\VSprojects\back\0\0')
    print(d.orign_path)