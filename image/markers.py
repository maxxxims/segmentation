import numpy as np
from collections import defaultdict


class Marker:
    def __init__(self, points: list = [], value: int = -1, dim: int = 2) -> None:
        """
            1 2
            3 4
        """
        if value < 0:
            self.points = []
            return None
        else:
            self.value = value
        
        if dim == 2:
            if len(points) == 8:
                self.x1, self.y1, self.x2, self.y2, self.x3, self.y3, self.x4, self.y4 = points
            elif len(points) == 4:
                self.x1, self.y1, self.x4, self.y4 = points
                self.x2 = self.x4
                self.y2 = self.y1
                self.x3 = self.x1
                self.y3 = self.y4



class MarkerContainer:
    def __init__(self, markers: list[Marker] = None, dim: int = 2) -> None:
        self.markers = markers
        self.dim = dim
        self._index()


    def add(self, marker: Marker) -> None:
        self.markers.append(marker)
        

    def from_file(self) -> list:
        if len(self.dim) == 2:
            markers = []
            with open(self.path_to_file, 'r') as file:
                for line in file.readlines():
                    if line[-1] == ' ':
                        line = line[:-1]
                    if len(line.split(' ')) == 9:
                        markers.append(Marker([int(line.split(' ')[0]), int(line.split(' ')[1]),
                                                int(line.split(' ')[2]), int(line.split(' ')[3]),], 
                                                int(line.split(' ')[4]), self.dim))


    def _index(self):
        self.value2marks = defaultdict(list)
        for i in range(len(self.markers)):
            self.value2marks[self.markers[i].value].append(i)