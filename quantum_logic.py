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
        self.ship_ids = ship_ids
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
        qubitsets = {}
        nset_current = 0
        field = -np.ones(shape=(self.field_size+1, self.field_size+1)).astype(int)
        for i, qship in enumerate(self.ships):
            new_set_idx = nset_current
            for shipcoords in qship.coordinates:
                x, y, hv = shipcoords
                fromx = x - 1 if x != 0 else 0
                fromy = y - 1 if y != 0 else 0
                tox = x + 2 if hv == 1 else x + 1 + qship.shape
                toy = y + 2 if hv == 0 else y + 1 + qship.shape

                for x_ in range(fromx, tox):
                    for y_ in range(fromy, toy):
                        if field[x_][y_] >= 0:
                            qset = QubitSet(idx=nset_current, ship_ids=qubitsets[field[x_][y_]].ship_ids + [i])
                            qubitsets[nset_current] = qset
                            qubitsets.pop(field[x_][y_])
                            field = draw_ids_on_ships(field, [self.ships[j] for j in qset.ship_ids], nset_current)
                            nset_current += 1
                            print(field)
                            print(qubitsets)

            if new_set_idx == nset_current:
                qset = QubitSet(idx=nset_current, ship_ids=[i])
                qubitsets[nset_current] = qset
                field = draw_ids_on_ships(field, [self.ships[i]], nset_current)
                nset_current += 1
                print(field)
            print(qubitsets)

        qubitsets_list = []
        for v in qubitsets.values():
            qubitsets_list.append(v)
        for i, qset in enumerate(qubitsets_list):
            qubitsets_list[i].idx = i
            qubitsets_list[i].nqubits = sum([self.ships[j].nqubits for j in qset.ship_ids])
        return qubitsets_list


def draw_ids_on_ships(field, ships, idx):
    for i, qship in enumerate(ships):
        for shipcoords in qship.coordinates:
            x, y, hv = shipcoords
            tox = x + 2 if hv == 1 else x + 1 + qship.shape
            toy = y + 2 if hv == 0 else y + 1 + qship.shape
            for x_ in range(x, tox - 1):
                for y_ in range(y, toy - 1):
                    field[x_][y_] = idx
    return field
