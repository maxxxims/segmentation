import numpy as np
from config import MARKER_TYPES


class Marker:
    def __init__(self, value: int = -1, dim: int = 2, type: str = MARKER_TYPES.EMPTY) -> None:
        self.value = value
        self.dim = dim
        self.type = type
        self.points = [].copy()
    def draw(self, data: np.array, color: int = 255) -> None:  ...
    def to_x_selection_index(self, height: int) -> list[int]:  ...
    def __str__(self):
        if self.type == MARKER_TYPES.RECTANGLE:
            return f'{self.x1} {self.y1} {self.x2} {self.y2} {self.x3} {self.y3} {self.x4} {self.y4} {self.value}'
        elif self.type == MARKER_TYPES.FILL:
            return f'{self.x1} {self.y1} {self.value}'




class MarkerRectangle2D(Marker):
    def __init__(self, points: list[int, int, int, int], value: int, dim: int = 2) -> None:
        super().__init__(value, dim, MARKER_TYPES.RECTANGLE)
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
    def __init__(self, points: list[int], value: int, dim: int = 2) -> None:
        """
            takes array like [x1, y1, x2, y2 ... ]  if x, y index of array:  y <-> x
        """
        super().__init__(value, dim, MARKER_TYPES.FILL)
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
        
