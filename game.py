from quantum_logic import Battleship


class GameField:
    def __init__(self, field_size=12, qbits=11, total_ships=10, ):
        self.field_size = field_size
        self.ships = []
        self.current_size = None
        self.current_ship = None
        self.qbits_total = qbits
        self.qbits_remaining = qbits
        self.ships_total = total_ships
        self.draw_in_progress = False

    def draw_next_ship(self, size):
        self.draw_in_progress = True
        if self.current_ship is not None or self.current_size is not None:
            if len(self.current_ship) == 0:
                return "No current ships placed"
            self.ships.append(Battleship(shape=self.current_size, coordinates=self.current_ship))
            self.qbits_remaining -= int(np.ceil(np.log2(len(self.current_ship))))
        if len(self.ships) >= self.ships_total:
            self.current_ship = []
            self.current_size = size

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
            pass

    def finished_drawing(self):
        self.draw_in_progress = False
