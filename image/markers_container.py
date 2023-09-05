from image.markers import *
from image.image import Image
from collections import defaultdict
import json
from PIL import Image as IMG
from config import MARKER_TYPES, MARKUP


class MarkerContainer:
    def __init__(self, markers: list[Marker] = [], dim: int = 2) -> None:
        self.markers = markers.copy()
        self.dim = dim
        self.value2marks = defaultdict(list)
        for i in range(len(self.markers)):
            self.value2marks[self.markers[i].value].append(i)


    def add(self, points: list, value: int, type: str = MARKER_TYPES.RECTANGLE) -> None:
        if type.lower() == MARKER_TYPES.RECTANGLE:
            self.markers.append(MarkerRectangle2D(points, value, self.dim))
        elif type.lower() == MARKER_TYPES.FILL:
            self.markers.append(MarkerFill2D(points, value, self.dim))
        self.value2marks[value].append(len(self.markers) - 1)


    def draw(self, data: np.array, color: int = 255) -> None:
        for marker in self.markers:
            marker.draw(data, color)


    def from_file(self, path_to_file: str) -> None:
        """
            open .json file
        """
        with open(path_to_file, 'r') as file:
            data = json.load(file)
            for point in data:
                if self.dim == point['dim']:
                    self.add(point['points'], point['value'], point['type'])


    def from_png(self, path_to_image: str, image: Image) -> None:
        """
            *.png file with markers for image file
                color to value look in config.config_markers
        """
        with IMG.open(path_to_image) as img:
            img.load()
            markers_mask = np.array(img)
        
        color2mark, value2point = MARKUP.get()
        markers_mask = np.array(list(map(lambda x: [color2mark[np.sum(el)]
                                                    if not (el[0] == el[1] == el[2]) and np.sum(el) in color2mark.keys()
                                                    else -1
                                                    for el in x ], markers_mask)))
        x_arr, y_arr = np.where(markers_mask >= 0)
        for x, y in zip(x_arr, y_arr):
            value2point[markers_mask[x, y]].append(y)
            value2point[markers_mask[x, y]].append(x)
        
        for key in value2point.keys():
            self.add(value2point[key], key, MARKER_TYPES.FILL)


    def with_value(self, value: int) -> list[Marker]:
        if value in self.value2marks.keys():
            return [self.markers[i] for i in self.value2marks[value]]
        else:
            return []
        
    def __getitem__(self, item: int):
        return self.markers[item]
        
    
    def __iter__(self):
        self.index_iter = 0
        return self
    
    def __next__(self):
        i = self.index_iter
        self.index_iter += 1
        if i >= len(self.markers) or len(self.markers) == 0:
            self.index_iter = 0
            raise StopIteration
        else:
            return self.markers[i]