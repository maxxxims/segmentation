from ..image import Image
from matplotlib import pyplot as plt
import json
import numpy as np
import os 





# def cut_image(img: Image, x1, y1, x2, y2):
#     path = r'C:\Users\maxxx\VSprojects\labeling\im_00001.png'
#     img = Image(path)
#     img.data = img.data[y1:y2, x1:x2]
#     img.show()
#     plt.imsave('cut.png', img.data, cmap='gray')



def save_json(y_1_class: list, x_1_class: list, y_0_class: list, x_0_class: list, 
              width0: int, height0: int, width: int, height: int,
              image_tag: str, original_image_name: str, image_path: str,
              original_image_url: str, annotated_image_url: str,
              file_name: str
              ):
    info_data = {
        'original_image_name': original_image_name,
        'image_tag': image_tag,
        'original_image_url': original_image_url,
        'annotated_image_url': annotated_image_url,
        'width0': width0,
        'height0': height0,
        'width': width,
        'height': height,
        'image_path': image_path,
        'y_1_class': y_1_class,
        'x_1_class': x_1_class,
        'y_0_class': y_0_class,
        'x_0_class': x_0_class
    }
    with open(f'data/{file_name}.json', 'w') as f:
        json.dump(info_data, f)


def show_slice(img: Image, h0, w0, h=300, w=300):
    img.data = img.data[h0:h0+h, w0:w0+w]
    print(f'shape = {img.data.shape}')
    img.show()


def cut_image(img: Image, img_annotated: Image, w0, h0, w, h, file_name: str):
    img.data = img.data[w0:w0+w, h0:h0+h]
    img_annotated.data = img_annotated.data[w0:w0+w, h0:h0+h]
    np.save(f'data/{file_name}.npy', img.data)
    np.save(f'data/{file_name}_annotated.npy', img_annotated.data)


def test_correctly(path_to_orig_img, path_to_cutted_img, w0, h0, w, h):
    img_orig = Image(path_to_orig_img)
    img = Image(data=np.load(path_to_cutted_img + '.npy'))
    print(f'shapes = {img.data.shape}, {img_orig.data[w0:w0+w, h0:h0+h].shape}')
    print((img.data == img_orig.data[w0:w0+w, h0:h0+h]).all())
    print(np.equal(img.data, img_orig.data[w0:w0+w, h0:h0+h]))
    print(f'len uncorrect = {np.sum(img.data != img_orig.data[w0:w0+w, h0:h0+h])}')
    # print(f'before = {len(img.data == 255)}')
    # img.data[img.data != img_orig.data[w0:w0+w, h0:h0+h]] = 255
    # print(f'after = {len(img.data == 255)}')
    img.show_images(1, 2, img, img_orig.data[w0:w0+w, h0:h0+h])

    

def save_pair():
    orig_img_path = r'C:\Users\maxxx\VSprojects\labeling\im_00001.png'
    annotated_img_path = r'C:\Users\maxxx\VSprojects\back\0\0\02. Segmented\00. Original\im_00001.png'
    img = Image(orig_img_path)
    img_annotated = Image(annotated_img_path)
    file_name = 'im_00001_900_1850_500_500'
    
    cut_image(img, img_annotated, 900, 1850, 500, 500, file_name=file_name)

    test_correctly(orig_img_path, f'save_img', 900, 1850, 500, 500,
                    )
    test_correctly(annotated_img_path, f'data/{file_name}_annotated', 900, 1850, 500, 500,
                    )


########################################################
MAIN_FOLDER = r'C:\Users\maxxx\VSprojects\back'
RELATIVE_GT_PATH = r'02. Segmented\00. Original'

def _save_annotation_json(width0: int, height0: int, width: int, height: int,
              image_tag: str, original_image_name: str, image_path: str,
              original_image_url: str, annotated_image_url: str,
              file_name: str):
    info_data = {
        'original_image_name': original_image_name,
        'image_tag': image_tag,
        'original_image_url': original_image_url,
        'annotated_image_url': annotated_image_url,
        'width0': width0,
        'height0': height0,
        'width': width,
        'height': height,
        'image_path': image_path,
    }
    with open(f'data/{file_name}.json', 'w') as f:
        json.dump(info_data, f, indent=4)


def make_configuration_file(cfg: dict):
    img_name = cfg['image_name']
    path_folder = cfg['folder_path']
    relative_img_path = cfg['relative_image_path']

    path_to_img    = os.path.join(MAIN_FOLDER, path_folder, relative_img_path, img_name)
    path_to_gt_img = os.path.join(MAIN_FOLDER, path_folder, RELATIVE_GT_PATH, img_name)
    img = Image(path_to_img)
    img_annotated = Image(path_to_gt_img)

    file_name = cfg['image_tag']

    height0, width0, height, width = 2060, 2140, 300, 300
    # height0, width0, height, width = 1070, 1270, 300, 300
    cfg['height0'] = height0
    cfg['width0'] = width0
    cfg['height'] = height
    cfg['width'] = width

    # img.show()
    # show_slice(img, height0, width0, height, width)
    # return 0


    cut_image(img, img_annotated, height0, width0, height, width, file_name=file_name)
    print('Print link to orig img')
    original_image_url = input()
    print('Print link to annotated img')
    annotated_image_url = input()

    cfg['original_image_url']  = original_image_url
    cfg['annotated_image_url'] = annotated_image_url

    with open(f'data/{file_name}.json', 'w') as f:
        json.dump(cfg, f, indent=2)
    

if __name__ == '__main__':
    cfg = {
        'folder_path': r'images\4',   #7, 5, 6
        'relative_image_path': r'01. Reconstructed\02. Angular Decimation\02. x4',
        'image_name': 'im_00001.png',
        'image_tag': 'ex2_300',

        # 'width0': 900,
        # 'height0': 1850,
        # 'width': 500,
        # 'height': 500,
    }
    make_configuration_file(cfg)
    # save_pair()
    # _save_annotation_json(width0=900, height0=1850, width=500, height=500, 
    #                       image_tag='im_00001_900_1850_500_500', original_image_name='im_00001.png',
    #                       image_path='original', 
    #                       original_image_url='https://disk.yandex.ru/d/q4nc_JjE8goTgA',
    #                       annotated_image_url='https://disk.yandex.ru/d/grX5vH64ORPHGA',
    #                       file_name='ex1_500')
    # file_name = 'im_00001_900_1850_500_500'
    # img = Image(data=np.load(f'data/{file_name}_annotated' + '.npy'))
    # img.show()
    # img.show()
    # show_slice(img, 900, 1850, 500, 500)
    
    
    # img.show(title='original')
    
    #cut_image(img, 1000, 1000, 1000+500, 1000+500)