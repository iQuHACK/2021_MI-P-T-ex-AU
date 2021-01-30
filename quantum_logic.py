import numpy as np
from typing import List, Tuple


class Battleship:
    def __init__(self, shape: int, coordinates: List[Tuple[int, int, int]]):
        self.shape = shape
        self.coordinates = coordinates
        self.damage = np.ones(shape)
        self.q_set = None


class QuantumGame:
    def __init__(self, ships: List[Battleship]):
        self.ships = ships

    def shoot_cells(self, coordinates: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        pass
