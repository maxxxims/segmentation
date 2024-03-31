from pathlib import Path
import json
import numpy as np
from backend import Image
import cv2


def cut_img(img: Image, h0, w0, h=300, w=300):
    img.data = img.data[h0:h0+h, w0:w0+w]
    
    
def draw_rectangle(img: Image, h0, w0, h=300, w=300, shift=1):
    cv2.rectangle(img.data, (w0 - shift, h0 - shift), (w0+w+shift, h0+h+shift), 255, 1)


def make_big_img(img: Image, radius: int, slice_radius: int, cfg: dict, path_to_save: Path,
                center_point=None, save:bool = True):
    if center_point is None:    center_point = (img.shape[0] // 2, img.shape[1] // 2)
    big_img_h0 = center_point[0] - radius
    big_img_w0 = center_point[1] - radius
    big_img_h = 2 * radius
    big_img_w = 2 * radius
    cfg['big_image'] = {
        'h0': big_img_h0,
        'w0': big_img_w0,
        'h': big_img_h,
        'w': big_img_w
    }
    
    cut_img(img, big_img_h0, big_img_w0, big_img_h, big_img_w)
    
    new_center_point = (img.shape[0] // 2, img.shape[1] // 2)
    small_img_h0 = new_center_point[0] - slice_radius
    small_img_w0 = new_center_point[1] - slice_radius
    small_img_h = 2 * slice_radius
    small_img_w = 2 * slice_radius
    
    cfg['small_image'] = {
        'relative': {'h0': small_img_h0, 'w0': small_img_w0, 'h': small_img_h, 'w': small_img_w},
        'absolute': {'h0': center_point[0] - slice_radius, 'w0': center_point[1] - slice_radius,
                     'h': 2 * slice_radius, 'w': 2 * slice_radius}
    }
    
    draw_rectangle(img, small_img_h0, small_img_w0, small_img_h, small_img_w)
    if save:
        image_full_path = str(path_to_save / f"{cfg['image_tag']}_full.npy")
        path_to_save.mkdir(parents=True, exist_ok=True)
        np.save(image_full_path, img.data)
        img.save(path_to_save / f"{cfg['image_tag']}_full.png")
        cfg['image_full_path'] = image_full_path
    else:
        img.show()
    return cfg


def save_gt_image(img_gt: Image, cfg: dict, save_path: Path):
    data = cfg['small_image']['absolute']
    cut_img(img_gt, data['h0'], data['w0'], data['h'], data['w'])
    annotatated_path = str(save_path / f"{cfg['image_tag']}_annotated.npy")
    np.save(annotatated_path, img_gt.data)
    img_gt.save(save_path / f"{cfg['image_tag']}_gt.png")
    cfg['annotatated_path'] = annotatated_path
    return cfg


def save_cfg(cfg: dict, save_path: Path):
    cfg_name = cfg['image_tag'] + '.json'
    with open(save_path / cfg_name, 'w') as file:
        json.dump(cfg, file, indent=2)
        

def cuut_one_img(img_number: int, img_save_name: int, center_point=None):
    cfg = {
        'folder_path': r'images\{}'.format(img_number),   #7, 5, 6
        'relative_image_path': r'01. Reconstructed\02. Angular Decimation\01. x2',
        'image_name': 'im_00001.png', #im_02086
        'image_tag': f'img{img_save_name}_500',
    }
    save_folder = Path('data')
    path_to_img = Path(r'C:\Users\maxxx\VSprojects\back\images') / f'{img_number}' / cfg['relative_image_path'] / 'im_00001.png'
    img = Image(path_to_img)
    cfg = make_big_img(img, radius=300, slice_radius=150, cfg=cfg, path_to_save=save_folder / 'input', center_point=center_point, save=True) 
    img_gt = Image(Path(r'C:\Users\maxxx\VSprojects\back\images\{}\02. Segmented\00. Original'.format(img_number)) / 'im_00001.png')
    cfg = save_gt_image(img_gt, cfg, save_folder / 'input')
    save_cfg(cfg, save_folder)
    # img_gt.show()


if __name__ == '__main__':
    ...
    # for i in range(6, 7):
    #    cuut_one_img(i)
    # center_point=(2715, 1495)#(1957, 1235)
    # cuut_one_img(0, 3, center_point=center_point)

    # path_to_img = Path(r'C:\Users\maxxx\VSprojects\back\images\0\01. Reconstructed\02. Angular Decimation\01. x2\im_00001.png')
    # img = Image(path_to_img)
    # img.show()
    # cfg = {}/
    # make_big_img(img, radius=300, slice_radius=150, cfg=cfg, save=False, center_point=(1957, 1235), path_to_save=None)
    #(1770, 2633-50)

    #img.show()
    # data = np.load(save_folder / 'input/img0_500_full.npy')
    # print(Image(data=data).shape)
    
    # data = np.load(save_folder / 'input/img0_500_annotated.npy')
    # print(Image(data=data).shape)