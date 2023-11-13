import numpy as np
import matplotlib.pyplot as plt
from backend.image import Image, Marker, MarkerRectangle2D, MarkerFill2D, MarkerContainer
from backend.filters import  filters_2dim as filters_2d
from backend.filters.filters import BaseFilter2D
# from backend.segmentation import SKSegmentation, Segmentation
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from backend import MarkerMakerRectangle2DBinary, Accuracy, Segmentation, Evaluator, MarkerBorder2D


OUTPUT_PATH = r'C:\Users\maxxx\VSprojects\back\0\0\result\0.png'


def test_marker_maker(path_to_image: str):
    """
        make markers from piece of segmented image (rectangle marker) and show the markers
    """
    image = Image(path_to_image=path_to_test_image, dim=2)
    # image.show()
    # print(image.data.shape)
    # print(image.data, image.data[0][0])

    p1 = (1957, 2106)
    p2 = (3388, 2937)
    marker_maker = MarkerMakerRectangle2DBinary(path_to_image, *p1, *p2)
    marker_maker.show_slice()
    markers = marker_maker.get_markers()

    for m in markers:
        image.draw_marker(m)
        image.show()
        image.reset()


def test_segmentation(path_to_orig_image: str, path_to_segmented_image: str):
    image = Image(path_to_image=path_to_test_image, dim=2)
    INFORMING = False
    if INFORMING:
        print(
            f'img shape = {image.shape()}, img data = {image.data[0]}'
        )
    p1 = (1957, 2106)
    p2 = (3388, 2937)
    marker_maker = MarkerMakerRectangle2DBinary(path_to_segmented_image, *p1, *p2)
    markers = marker_maker.get_markers()
    sgm = Segmentation(LogisticRegression())
    sgm.segmentate(image, markers, [filters_2d.MedianFilter(size=5), filters_2d.GaussianFilter(5),
                               filters_2d.BaseFilter2D()], test_markers=True)
    # image.show_segments(markers[0])
    # image.show_segments(markers[1], fill_color=0)
    image.show()
    if INFORMING:
        print(sgm.feature_weights())
        print(
            f'sgm shape = {image.shape()}, sgm data = {image.data}'
        )
    #image.save(OUTPUT_PATH)
    ground_truth = Image(path_to_image=path_to_segmented_image, dim=2)
    ground_truth.show()
    print(Accuracy.get_score(image, ground_truth))
    Accuracy.show_diffrence(image, ground_truth)


def test_filter(path_to_orig_image: str, path_to_segmented_image: str):
    image = Image(path_to_image=path_to_orig_image, dim=2)
    offside = np.sum(image.data == 85)
    print(f'offside = {offside}, {len(image.data[image.data == 85])}')
    #image.data[image.data == 85] = 0
    # image.show()
    # return 1
    p1 = (1957, 2106)
    p2 = (3388, 2937)

    p1 = (1957, 2106)
    p2 = (1957 + 1000, 2106 + 1000)

    marker_maker = MarkerMakerRectangle2DBinary(path_to_segmented_image, *p1, *p2)
    markers = marker_maker.get_markers()
    
    filters =[filters_2d.MedianFilter(size=5), filters_2d.GaussianFilter(15), filters_2d.LaplacianDifference(),
                              filters_2d.BaseFilter2D()]
    #filters = [filters_2d.BaseFilter2D()]
    sgm = Segmentation(LogisticRegression(), image, filters)
    
    # for i in range(len(filters)):
    #     plt.imshow(np.transpose(sgm.features, (2, 0, 1))[i], cmap='gray')
    #     plt.show()



    sgm.fit(markers)
    result = sgm.predict()
    result.data = result.data * 255
    result.show()
    ground_truth = Image(path_to_image=path_to_segmented_image, dim=2)
    # print(result.data)
    
    print(Accuracy.get_score(result, ground_truth, offside=offside))
    Accuracy.show_diffrence(result, ground_truth)
    # image.show()
    

def test_del_border(path_to_orig_image: str, path_to_border_image: str):
    """
        open border img and show the border
    """
    image_orig = Image(path_to_image=path_to_orig_image, dim=2)
    image_border = Image(path_to_image=path_to_border_image, dim=2)
    yellow_color = [255, 242, 0, 255]
    print(f'border value = {image_border.data.shape}')
    image_border.data[(
        image_border.data[:, :, 0] == yellow_color[0]
        ) & (image_border.data[:, :, 1] == yellow_color[1]) & (image_border.data[:, :, 2] == yellow_color[2])] = [0, 0, 0, 255]
    image_border.data = image_border.data[:, :, 0]
    image_border.show()
    ...

def test_metrics_evaluator(path_to_orig_image: str, path_to_segmented_img: str, path_to_border_image: str):
    image = Image(path_to_image=path_to_orig_image, dim=2)

    p1 = (1957, 2106)
    p2 = (1957 + 100, 2106 + 100)
    marker_maker = MarkerMakerRectangle2DBinary(path_to_segmented_image, *p1, *p2)
    markers = marker_maker.get_markers()
    filters =[filters_2d.MedianFilter(size=5), filters_2d.GaussianFilter(15), filters_2d.LaplacianDifference(),
                              filters_2d.BaseFilter2D()]
    # filters = [filters_2d.BaseFilter2D()]
    sgm = Segmentation(LogisticRegression(), image, filters)
    sgm.fit(markers)
    result = sgm.predict()
    result.data = result.data * 255

    ground_truth = Image(path_to_image=path_to_segmented_image, dim=2)
    border_marker = MarkerBorder2D(Image(path_to_image=path_to_border_image, dim=2))

    # image.data[border_marker.get_indexes()[1], border_marker.get_indexes()[0]] = 0
    image.draw_marker(border_marker)
    image.show(title="Image with no border") 

    Evaluator.evaluate(result, ground_truth, markers, border_marker, Accuracy)


def open_output():
    image = Image(path_to_image=OUTPUT_PATH, dim=2)
    image.show()
    print(image.shape())
    


if __name__ == '__main__':
    path_to_test_image      = r"C:\Users\maxxx\VSprojects\back\0\0\01. Reconstructed\00. Original\im_00001.png"
    path_to_test_image_bad  = r'C:\Users\maxxx\VSprojects\back\0\0\01. Reconstructed\02. Angular Decimation\02. x4\im_00001.png'
    path_to_segmented_image = r"C:\Users\maxxx\VSprojects\back\0\0\02. Segmented\00. Original\im_00001.png"
    path_to_border_img      = r"C:\Users\maxxx\VSprojects\back\0\0\border\border00001.png"
    #test_marker_maker(path_to_segmented_image)

    #test_segmentation(path_to_orig_image=path_to_test_image, path_to_segmented_image=path_to_segmented_image)
    #open_output()
    #test_filter(path_to_orig_image=path_to_test_image, path_to_segmented_image=path_to_segmented_image)

    #test_filter(path_to_orig_image=path_to_test_image_bad, path_to_segmented_image=path_to_segmented_image)

    # test_del_border(path_to_orig_image=path_to_test_image, path_to_border_image=path_to_border_img)

    test_metrics_evaluator(path_to_orig_image=path_to_test_image_bad, path_to_segmented_img=path_to_segmented_image, path_to_border_image=path_to_border_img)