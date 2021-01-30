from quantum_logic import Battleship, QuantumGame


class GameField:
    def __init__(self, draw_next_ship, color_cell, change_qubits_left, field_size=10, qbits=11):
        self.field_size = field_size
        self.ships = []
        self.current_ship = []
        self.qbits_total = qbits
        self.qbits_remaining = qbits
        self.draw_in_progress = True
        self.draw_next_ship = draw_next_ship
        self.color_cell = color_cell
        self.change_qubits_left = change_qubits_left
        self.qgame = None
        self.ship_num = 0
        self.max_qbits_per_ship = 3
        self.ship_sizes = (4, 3, 3, 2, 2, 2, 1, 1, 1, 1)
        self.ship_colors = ('#E43F6F', '#93E1D8', '#1C7C54', '#E9806E', '#EEFC57',
                            "#2660a4", "#c47335", "#eff0d1", "#77ba99", "#56351e")
        self.call_draw_next_ship()

    def call_draw_next_ship(self):
        self.draw_next_ship(
            size=self.ship_sizes[self.ship_num] if self.ship_num < len(self.ship_sizes) else 0,
            color=self.ship_colors[self.ship_num] if self.ship_num < len(self.ship_colors) else None,
            is_last=self.ship_num + 1 == len(self.ship_sizes))

    def next_ship_clicked(self):
        self.draw_in_progress = True
        if len(self.current_ship) == 0:
            raise UserWarning('No ships placed')
        self.ships.append(Battleship(shape=self.ship_sizes[self.ship_num], coordinates=self.current_ship))
        self.current_ship = []
        self.ship_num += 1
        self.call_draw_next_ship()
        if self.ship_num == len(self.ship_sizes):
            self.draw_in_progress = False

    # 0 - vertical, 1 - horizontal
    def cell_clicked(self, x, y, orientation):
        if self.draw_in_progress:
            if len(self.current_ship) == 8:
                raise UserWarning('You can only use three cubits for a ship')
            ship_sz = self.ship_sizes[self.ship_num]
            if orientation == 0 and x + ship_sz > self.field_size or \
                    orientation == 1 and y + ship_sz > self.field_size:
                raise UserWarning('You cannot place a ship with this orientation here')

            sz = len(self.current_ship)
            if sz > 1 and (sz & (sz - 1)) == 0:
                if self.qbits_remaining == 0:
                    raise UserWarning('You have no qubits left')
                self.qbits_remaining -= 1
                self.change_qubits_left(self.qbits_remaining)

            xx, yy = x, y
            for i in range(ship_sz):
                self.color_cell(xx, yy, self.ship_colors[self.ship_num])
                if orientation == 0:
                    xx += 1
                else:
                    yy += 1

            self.current_ship.append((x, y, orientation))
        else:
            if self.qgame is None:
                self.qgame = QuantumGame(self.ships)
