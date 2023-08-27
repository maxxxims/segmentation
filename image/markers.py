import numpy as np
from collections import defaultdict
import json


RECTANGLE = 'rectangle'
FILL = 'fill'
EMPTY = 'empty'


class Marker:
    def __init__(self, value: int = -1, dim: int = 2, type: str = EMPTY) -> None:
        self.value = value
        self.dim = dim
        self.type = type
        self.points = [].copy()
    def draw(self, data: np.array, color: int = 255) -> None:
        ...
    def to_x_selection_index(self, height: int) -> list[int]:
        ...
    def __str__(self):
        if self.type == RECTANGLE:
            return f'{self.x1} {self.y1} {self.x2} {self.y2} {self.x3} {self.y3} {self.x4} {self.y4} {self.value}'
        elif self.type == FILL:
            return f'{self.x1} {self.y1} {self.value}'
        
        
class MarkerRectangle2D(Marker):
    def __init__(self, points: list[int], value: int, dim: int = 2) -> None:
        super().__init__(value, dim, RECTANGLE)
        if len(points) == 8:
            self.x1, self.y1, self.x2, self.y2, self.x3, self.y3, self.x4, self.y4 = points
        elif len(points) == 4:
            self.x1, self.y1, self.x4, self.y4 = points
            self.x2 = self.x4
            self.y2 = self.y1
            self.x3 = self.x1
            self.y3 = self.y4
        self.points = [(self.x1, self.y1), (self.x2, self.y2), (self.x3, self.y3), (self.x4, self.y4)]


    def draw(self, data: np.array, color: int = 255) -> None:
        data[self.y1 : self.y4 + 1, self.x1 : self.x4 + 1] = 255


    def to_x_selection_index(self, height: int) -> list[int]:
        res = []
        for x in range(self.x1, self.x4 + 1):                       # +1 ?
            for y in range(self.y1, self.y4 + 1):
                res.append(x * height + y)
        return res

class MarkerFill2D(Marker):
    def __init__(self, points: list[int, int, int, int], value: int, dim: int = 2) -> None:
        super().__init__(value, dim, FILL)
        self.x1 = points[0]
        self.y1 = points[1]
        self.points = [(points[2 * i], points[2 * i + 1]) for i in range(len(points) // 2)]


    def draw(self, data: np.array, color: int = 255) -> None:
        for x, y in self.points:
            data[y, x] = 255


    def to_x_selection_index(self, height: int) -> list[int]:
        res = []
        for x, y in self.points:
            res.append(x * height + y)
        return res


class MarkerContainer:
    def __init__(self, markers: list[Marker] = [], dim: int = 2) -> None:
        self.markers = markers.copy()
        self.dim = dim
        self.value2marks = defaultdict(list)
        for i in range(len(self.markers)):
            self.value2marks[self.markers[i].value].append(i)


    def add(self, points: list, value: int, type: str = RECTANGLE) -> None:
        if type.lower() == RECTANGLE:
            self.markers.append(MarkerRectangle2D(points, value, self.dim))
        elif type.lower() == FILL:
            self.markers.append(MarkerFill2D(points, value, self.dim))
        self.value2marks[value].append(len(self.markers) - 1)


    def draw(self, data: np.array, color: int = 255) -> None:
        for marker in self.markers:
            marker.draw(data, color)


    def from_file(self, path_to_file: str) -> None:
        """
            file.txt with lines: 
                x1 y1 x4 y4 value;
        if self.dim == 2:
            markers = []
            with open(path_to_file, 'r') as file:
                for line in file.readlines():
                    line = list(map(int, line[:line.find(';')].split(' ')))
                    if len(line) == 5:
                        self.add(line[:-1], line[-1], type = RECTANGLE)
                    if len(line) > 5:
                        self.add(line[:-1], line[-1], type = FILL)
        """
        with open(path_to_file, 'r') as file:
            data = json.load(file)
            for point in data:
                if self.dim == point['dim']:
                    self.add(point['points'], point['value'], point['type'])
                

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
        

""" old version
class Marker:
    def __init__(self, points: list = [], value: int = -1, dim: int = 2, type: str = RECTANGLE) -> None:
    
            1 2  or 1 .
            3 4     . 4
    
        self.dim = dim
        if value < 0:
            self.points = []
            self.type = EMPTY
            return None
        else:
            self.value = value
            self.type = type
        if dim == 2:
            if len(points) == 8 and type == RECTANGLE:
                self.x1, self.y1, self.x2, self.y2, self.x3, self.y3, self.x4, self.y4 = points
            elif len(points) == 4  and type == RECTANGLE:
                self.x1, self.y1, self.x4, self.y4 = points
                self.x2 = self.x4
                self.y2 = self.y1
                self.x3 = self.x1
                self.y3 = self.y4
            elif type == FILL:
                self.x1 = points[0]
                self.y1 = points[1]
                self.points = [(points[2 * i], points[2 * i + 1]) for i in range(len(points) // 2)]

            
    def draw(self, data: np.array, color: int = 255) -> None:
        if self.type == RECTANGLE:
            data[self.y1 : self.y4 + 1, self.x1 : self.x4 + 1] = 255
        elif self.type == FILL:
            for x, y in self.points:
                data[y, x] = 255


    def __str__(self):
        if self.type == RECTANGLE:
            return f'{self.x1} {self.y1} {self.x2} {self.y2} {self.x3} {self.y3} {self.x4} {self.y4} {self.value}'
        elif self.type == FILL:
            return f'{self.x1} {self.y1} {self.value}'


    def to_x_selection_index(self, height: int) -> list[int]:
        res = []
        if self.type == 'rectangle':
            for x in range(self.x1, self.x4 + 1):                       # +1 ?
                for y in range(self.y1, self.y4 + 1):
                    res.append(x * height + y)
        elif self.type == 'fill':
            for x, y in self.points:
                res.append(x * height + y)
        return res
"""