import numpy as np
from typing import List, Tuple


class Battleship:
    def __init__(self, shape: int, coordinates: List[Tuple[int, int, int]]):
        self.shape = shape
        self.coordinates = coordinates
        self.damage = np.ones(shape)
        self.q_set = None


class QuantumGame:
    def __init__(self, ships: List[Battleship], default_shoots_number: int = 5, field_size: int = 10):
        self.ships = ships
        self.default_shoots_number = default_shoots_number
        self.field_size = field_size

    def shoot_cells(self, coordinates: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        pass

    def get_shoots_number(self):
        return self.default_shoots_number
