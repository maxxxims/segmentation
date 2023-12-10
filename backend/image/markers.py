import numpy as np

from backend.config import MARKER_TYPES
from ..config import MARKER_TYPES


class Marker:
    def __init__(self, value: int = -1, dim: int = 2, type: str = MARKER_TYPES.EMPTY) -> None:
        self.value = value
        self.dim = dim
        self.type = type
        self.points = [].copy()

    def draw(self, data: np.array, color: int = 255) -> None:  ...

    def to_x_selection_index(self, height: int) -> list[int]:  ...
    
    def get_indexes(self):
        return self.x_indexes, self.y_indexes

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
        self.points = np.array([(points[2 * i], points[2 * i + 1]) for i in range(len(points) // 2)])


    def draw(self, data: np.array, color: int = 255) -> None:
        for x, y in self.points:
            data[y, x] = color


    def to_x_selection_index(self, height: int) -> list[int]:
        res = []
        for x, y in self.points:
            res.append(x * height + y)
        return res
    
    def get_indexes(self):
        x_indexes, y_indexes = self.points.reshape(-1, 2).T
        return (x_indexes, y_indexes)
    


class MarkerBorder2D(Marker):
    """
        markup the border
    """
    INNER_COLOR = [255, 242, 0, 255]
    def __init__(self, image_border, where='outer') -> None:
        """
            :param image_border: image with border
            :param where: 'inner' or 'outer' in what are the border
        """
        mask = ((
            image_border.data[:, :, 0] == self.INNER_COLOR[0]
            ) & (image_border.data[:, :, 1] == self.INNER_COLOR[1]) & (image_border.data[:, :, 2] == self.INNER_COLOR[2]))
        
        if where == 'outer':
            mask = ~mask
        super().__init__()
        (self.y_indexes, self.x_indexes) = np.where(mask)

    
    def draw(self, data: np.array, color: int = 0) -> None:
        data[self.y_indexes, self.x_indexes] = color

    


class MarkerByPoints2D(Marker):
    def __init__(self, x_indexes: list, y_indexes: list, value: int) -> None:
        super().__init__(value, 2)
        self.x_indexes = x_indexes
        self.y_indexes = y_indexes

    def draw(self, data: np.array, color: int = 0) -> None:
        data[self.y_indexes, self.x_indexes] = color