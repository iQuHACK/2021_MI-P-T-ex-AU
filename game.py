import numpy as np

from quantum_logic import Battleship, QuantumGame


class GameField:
    def __init__(self, draw_next_ship, color_cell, field_size=12, qbits=11, max_qbits_per_ship=3,
                 ship_sizes=(4, 3, 3, 2, 2, 2, 1, 1, 1, 1), nshoots_default=5):
        self.field_size = field_size
        self.ships = []
        self.nship_current = None
        self.current_ship = None
        self.qbits_total = qbits
        self.qbits_remaining = qbits
        self.qbits_per_ship = max_qbits_per_ship
        self.ship_sizes = ship_sizes
        self.draw_in_progress = False
        self.draw_next_ship = draw_next_ship
        self.color_cell = color_cell
        self.qgame = None
        self.nshoots_default = nshoots_default

    def next_ship_clicked(self):
        self.draw_in_progress = True
        if self.nship_current is None:
            self.nship_current = 0
        else:
            if len(self.current_ship) == 0:
                return "No current ships placed"
            self.ships.append(Battleship(shape=self.ship_sizes[self.nship_current], coordinates=self.current_ship))
            self.qbits_remaining -= int(np.ceil(np.log2(len(self.current_ship))))
        self.current_ship = []
        self.nship_current += 1
        if self.nship_current < len(self.ship_sizes):
            self.draw_next_ship(size=self.ship_sizes[self.nship_current])

    # 0 - horizontal, 1 - vertical
    def cell_clicked(self, x, y, orientation=None):
        if self.draw_in_progress:
            if orientation is None:
                return "Provide orientation"
            self.current_ship.append((x, y, orientation))
            if len(self.current_ship) > 1 and 2**self.qbits_remaining < len(self.current_ship):
                self.draw_in_progress = False
                return "No qbits left"
        else:
            if self.qgame is None:
                self.qgame = QuantumGame(self.ships, self.nshoots_default)
