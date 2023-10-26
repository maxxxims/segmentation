import numpy as np


class MARKER_TYPES:
    RECTANGLE = 'rectangle'
    FILL = 'fill'
    EMPTY = 'empty'


class MARKUP:
    def __init__(self, markmarkers_masker: np.array) -> None:
        """
            red - 1;  green - 0
        """
        self.color2mark = {
            237 + 28 + 36 + 255: 1, 34 + 177 + 76 + 255: 0
        }
        self.value2point = {value: [] for value in self.color2mark.values()}

    def get(self) -> tuple[dict[int, int], dict[int, list[int]]]:
        return (self.color2mark, self.value2point)
    
    name = 'Hello world!'