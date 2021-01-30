import numpy as np
from typing import List, Tuple


class Battleship:
    def __init__(self, shape: int, coordinates: List[Tuple[int, int, int]]):
        self.shape = shape
        self.coordinates = coordinates
        self.nqubits = None
        self.damage = np.ones(shape)
        self.q_set = None


class QubitSet:
    def __init__(self, idx: int, ship_ids: List[int]):
        self.idx = idx
        self.nqubits = 0
        self.ship_ids = []
        self.intersection_ids = []


class QuantumGame:
    def __init__(self, ships: List[Battleship], default_shoots_number: int, field_size: int):
        self.ships = ships
        for i, ship in enumerate(ships):
            self.ships[i].nqubits = int(np.ceil(np.log2(len(ship.coordinates))))
        self.default_shoots_number = default_shoots_number
        self.field_size = field_size

    def shoot_cells(self, coordinates: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        pass

    def get_shoots_number(self):
        return self.default_shoots_number

    def qubit_sets_from_ships(self) -> List[QubitSet]:
        qubitsets = []
        field = -np.ones(shape=(self.field_size+1, self.field_size+1))
        for i, qship in enumerate(self.ships):
            for j, shipcoords in enumerate(qship.coordinates):
                x, y, hv = shipcoords
                fromx = x - 1 if x != 0 else 0
                fromy = y - 1 if y != 0 else 0
                for x_ in range(fromx, x + 1 + qship.shape * (1 - hv)):
                    for y_ in range(fromy, y + 1 + qship.shape * hv):
                        if field[x_][y_] < 0:
                            field[x_][y_] = len(qubitsets)
                            qset = QubitSet(idx=len(qubitsets), ship_ids=[i])
                            qubitsets.append(QubitSet)
                        else:
                            pass

