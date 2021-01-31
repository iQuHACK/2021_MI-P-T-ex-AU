import numpy as np
import qiskit
import re
from typing import List, Tuple

from util import draw_ids_on_ships


class QuantumCircuits:
    def __init__(self, qc_type = 'qasm_simulator'):
        if qc_type == 'qasm_simulator':
            self.backend = qiskit.BasicAer.get_backend('qasm_simulator')
       #write other types of backends
    
    def my_bin(self, el:int, n:int) -> str:
        return "0"*(n -  len(bin(el)[2:])) + bin(el)[2:]

    def create_psi(self, ships, qset) -> List[str]:
        self.nqubits = qset.nqubits
        self.intersection_ids = qset.intersection_ids
        self.possible_psi = [self.my_bin(i,self.nqubits) for i in np.arange(2**self.nqubits)]

        ships_nq = {}
        ship_start_pos = {}
        ships_n_re = {}
        pos = 0
        for ship in qset.ship_ids:
            ships_nq[ship] = ships[ship].nqubits
            ships_n_re = len(ships[ship].coordinates)
            ship_start_pos[ship] = pos
            pos += ships_nq[ship]
            

        for ship in qset.ship_ids:
            for i in range(ships_n_re[ship], 2**ships_nq[ship] ):
                pattern = re.compile(
                    "[0,1]{%i}" % ship_start_pos[ship] + 
                    self.my_bin(i, ships_nq[ship]) + 
                    "[0,1]{%i}"%(qset.nqubits - ship_start_pos[ship] - ships_nq[ship] ) )
                rm_elements = []
                for psi in self.possible_psi:
                    if re.match(pattern, psi):
                        rm_elements.append(psi)
                for el in rm_elements:
                    self.possible_psi.remove(el)
                                 
        for intersection in qset.intersection_ids:
            print(intersection)
            if ship_start_pos[intersection[0][0]] < ship_start_pos[intersection[1][0]]:
                id_0, q_id_0 = intersection[0]
                id_1, q_id_1 = intersection[1]
            else:
                id_1, q_id_1 = intersection[0]
                id_0, q_id_0 = intersection[1]
            pattern = re.compile(
                "[0,1]{%i}" % ship_start_pos[id_0] + 
                self.my_bin(q_id_0, ships_nq[id_0]) + 
                "[0,1]{%i}"%(ship_start_pos[id_1] - ships_nq[id_0] - ship_start_pos[id_0] ) +
                self.my_bin(q_id_1, ships_nq[id_1]) + 
                "[0,1]{%i}"%(qset.nqubits - ship_start_pos[id_1] - ships_nq[id_1] ))
           
        rm_elements = []
        for psi in self.possible_psi:
            if re.match(pattern, psi):
                rm_elements.append(psi)

        for el in rm_elements:
            self.possible_psi.remove(el)
    
    def change_sign(self, var: str):
        for i, v_i in enumerate(var[::-1]):
            if v_i == "0":
                self.qc.x(self.q_reg[i])
                   
    def recursion_qubit(self, path: str, possible_psi: List[str]):
        last = [i[-1] for i in possible_psi[:]]
        if "1" in last and "0" in last:
            if path == "":
                self.qc.h(self.q_reg[0])
            else:
                self.change_sign(path)
                self.qc.mct(self.q_reg[:len(path)], self.aux_reg[0])
                self.qc.ch(self.aux_reg[0], self.q_reg[len(path)])
                self.qc.mct(self.q_reg[:len(path)], self.aux_reg[0])
                self.change_sign(path)
        elif "1" in last:
            if path == "":
                self.qc.x(self.q_reg[0])
            else:
                self.change_sign(path)
                self.qc.mct(self.q_reg[:len(path)], self.q_reg[len(path)])
                self.change_sign(path) 
                   
        for val in np.unique(last):
            if len(possible_psi[0]) > 1:
                new_psi = [s[:-1] for s in possible_psi if s[-1]==val]
                self.recursion_qubit(val + path, new_psi)
                   
    def create_qc(self):
        self.q_reg = qiskit.QuantumRegister(self.nqubits)
        self.aux_reg = qiskit.QuantumRegister(1, "aux")
        self.c_reg = qiskit.ClassicalRegister(self.nqubits)
        self.qc = qiskit.QuantumCircuit(self.q_reg, self.aux_reg, self.c_reg)
                   
        self.recursion_qubit("", self.possible_psi)
        self.qc.measure(self.q_reg , self.c_reg)
                   
    def run_qc(self):
        job = qiskit.execute(self.qc, self.backend, shots=10000) #, seed_simulator = 3
        result = job.result()
        self.count = result.get_counts()


class Battleship:
    def __init__(self, shape: int, coordinates: List[Tuple[int, int, int]]):
        self.shape = shape
        self.coordinates = coordinates
        self.nqubits = None
        self.damage = np.ones(shape)
        self.q_set = None


class QubitSet:
    def __init__(self, idx: int, ship_ids: List[int], intersection_ids=None, nqubits=0):
        self.idx = idx
        self.nqubits = nqubits
        self.ship_ids = ship_ids
        self.intersection_ids: List[Tuple[Tuple[int, int], Tuple[int, int]]] = \
            intersection_ids if intersection_ids is not None else []

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.ship_ids == other.ship_ids and \
                   sorted(self.intersection_ids) == sorted(other.intersection_ids) and \
                   self.nqubits == other.nqubits
        else:
            return False


class QuantumGame:
    def __init__(self, ships: List[Battleship], default_shoots_number: int, field_size: int):
        self.ships = ships
        for i, ship in enumerate(self.ships):
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
        field = -100 * np.ones(shape=(self.field_size+1, self.field_size+1)).astype(int)
        for i, qship in enumerate(self.ships):
            new_set_idx = nset_current
            for j, shipcoords in enumerate(qship.coordinates):
                x, y, hv = shipcoords
                fromx = x - 1 if x != 0 else 0
                fromy = y - 1 if y != 0 else 0
                tox = x + 2 if hv == 0 else x + 1 + qship.shape
                toy = y + 2 if hv == 1 else y + 1 + qship.shape

                for x_ in range(fromx, tox):
                    for y_ in range(fromy, toy):
                        fvalue = field[x_][y_]
                        if fvalue >= 0 and i not in qubitsets[fvalue].ship_ids:
                            qset = QubitSet(idx=nset_current, ship_ids=qubitsets[fvalue].ship_ids + [i])
                            qubitsets[nset_current] = qset
                            qubitsets.pop(fvalue)
                            field = draw_ids_on_ships(field, [self.ships[k] for k in qset.ship_ids], nset_current)
                            nset_current += 1

            if new_set_idx == nset_current:
                qset = QubitSet(idx=nset_current, ship_ids=[i])
                qubitsets[nset_current] = qset
                field = draw_ids_on_ships(field, [self.ships[i]], nset_current)
                nset_current += 1
            # print(field)

        return self._construct_qubitset_list(qubitsets)

    def _construct_qubitset_list(self, qubitsets):
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
                    qubitsets_list[i].intersection_ids += self._get_ship_intersections(idx1, idx2)
        return qubitsets_list

    def _get_ship_intersections(self, idx1, idx2):
        qship1, qship2 = self.ships[idx1], self.ships[idx2]
        result = []
        for i, (x1, y1, hv1) in enumerate(qship1.coordinates):
            for j, (x2, y2, hv2) in enumerate(qship2.coordinates):
                fromx = x1 - 1 if x1 != 0 else 0
                fromy = y1 - 1 if y1 != 0 else 0
                tox = x1 + 2 if hv1 == 0 else x1 + 1 + qship1.shape
                toy = y1 + 2 if hv1 == 1 else y1 + 1 + qship1.shape
                x2end, y2end = x2 + hv2 * (qship2.shape - 1), y2 + (1 - hv2) * (qship2.shape - 1)
                if (fromx <= x2 < tox and fromy <= y2 < toy) or (fromx <= x2end < tox and fromy <= y2end < toy):
                    result.append(((idx1, i), (idx2, j)))
        return result
