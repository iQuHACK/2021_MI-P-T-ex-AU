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
        self.intersection_ids: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []


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
            for j, shipcoords in enumerate(qship.coordinates):
                x, y, hv = shipcoords
                fromx = x - 1 if x != 0 else 0
                fromy = y - 1 if y != 0 else 0
                tox = x + 2 if hv == 1 else x + 1 + qship.shape
                toy = y + 2 if hv == 0 else y + 1 + qship.shape

                for x_ in range(fromx, tox):
                    for y_ in range(fromy, toy):
                        fvalue = field[x_][y_]
                        if fvalue >= 0 and i not in qubitsets[fvalue].ship_ids:
                            qset = QubitSet(idx=nset_current, ship_ids=qubitsets[fvalue].ship_ids + [i])
                            qubitsets[nset_current] = qset
                            qubitsets.pop(fvalue)
                            field = draw_ids_on_ships(field, [self.ships[k] for k in qset.ship_ids], nset_current)
                            nset_current += 1
                            # print(field)
                            # print(qubitsets)

            if new_set_idx == nset_current:
                qset = QubitSet(idx=nset_current, ship_ids=[i])
                qubitsets[nset_current] = qset
                field = draw_ids_on_ships(field, [self.ships[i]], nset_current)
                nset_current += 1
            print(field)

        return self.set_intersections(qubitsets)

    def set_intersections(self, qubitsets):
        qubitsets_list = []
        for v in qubitsets.values():
            qubitsets_list.append(v)
        for i, qset in enumerate(qubitsets_list):
            qubitsets_list[i].idx = i
            qubitsets_list[i].nqubits = sum([self.ships[j].nqubits for j in qset.ship_ids])
            for j in qset.ship_ids:
                self.ships[j].q_set = i
            for j, idx1 in enumerate(qset.ship_ids):
                for idx2 in qset.ship_ids[j+1:]:
                    qubitsets_list[i].intersection_ids += self.get_ship_intersections(idx1, idx2)
        return qubitsets_list

    def get_ship_intersections(self, idx1, idx2):
        qship1, qship2 = self.ships[idx1], self.ships[idx2]
        result = []
        for i, (x1, y1, hv1) in enumerate(qship1.coordinates):
            for j, (x2, y2, hv2) in enumerate(qship2.coordinates):
                fromx = x1 - 1 if x1 != 0 else 0
                fromy = y1 - 1 if y1 != 0 else 0
                tox = x1 + 2 if hv1 == 1 else x1 + 1 + qship1.shape
                toy = y1 + 2 if hv1 == 0 else y1 + 1 + qship1.shape
                x2end, y2end = x2 + (1 - hv2) * qship2.shape, y2 + hv2 * qship2.shape
                if (fromx <= x2 < tox and fromy <= y2 < toy) or (fromx <= x2end < tox and fromy <= y2end < toy):
                    result.append(((idx1, i), (idx2, j)))
        return result


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
