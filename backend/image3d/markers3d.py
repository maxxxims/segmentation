from backend.config import MARKER_TYPES
from ..image import Image, Marker
import numpy as np


class MarkerPoints3D(Marker):
    def __init__(self, x_indexes: np.ndarray, y_indexes: np.ndarray, z_indexes: np.ndarray,
                  type: str = MARKER_TYPES.EMPTY, value: int = -1, dim: int = 3) -> None:
        super().__init__(value, dim, type)
        self.x_indexes = x_indexes
        self.y_indexes = y_indexes
        self.z_indexes = z_indexes
    

    def draw(self, data: np.array, color: int = 255) -> None:
        data[self.z_indexes, self.y_indexes, self.x_indexes] = color
    
    def get_indexes(self):
        return self.x_indexes, self.y_indexes, self.z_indexes
    

