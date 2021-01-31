from quantum_logic import Battleship, QuantumGame


class GameField:
    def __init__(self, controller, field_size=10, qbits=11, default_shoots_number=5):
        self.field_size = field_size
        self.ships = []
        self.current_ship = []
        self.qbits_total = qbits
        self.qbits_remaining = qbits
        self.draw_in_progress = True
        self.controller = controller
        self.default_shoots_number = default_shoots_number
        self.qgame = None
        self.ship_num = 0
        self.max_qbits_per_ship = 3
        self.guesses = 0
        self.selected_cells = []
        self.cells_per_guess = 5
        self.ship_sizes = (4, 3, 2, 2, 1, 1)
        self.ship_colors = ('#E43F6F', '#93E1D8', '#1C7C54', '#E9806E', '#EEFC57',
                            "#2660a4", "#c47335", "#eff0d1", "#77ba99", "#56351e")
        self.miss_color = '#8fcefd'
        self.injured_color = '#ec3520'
        self.killed_color = '#3a0a04'
        self.call_draw_next_ship()

    def call_draw_next_ship(self):
        self.controller.draw_next_ship(
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
            self.controller.init_guessing()

    def cell_clicked_guessing(self, x, y):
        if self.qgame is None:
            self.qgame = QuantumGame(self.ships,
                                     default_shoots_number=self.default_shoots_number,
                                     field_size=self.field_size)
        # TODO exit if cell is already shot
        if (x, y) in self.selected_cells:
            self.selected_cells.pop(self.selected_cells.index((x, y)))
            self.controller.color_cell_guessing(x, y, 'white')
        else:
            if len(self.selected_cells) == self.cells_per_guess:
                raise UserWarning("You don't have any cells left this guess")
            self.selected_cells.append((x, y))
            self.controller.color_cell_guessing(x, y, 'grey')
        self.controller.change_cells_left(self.default_shoots_number - len(self.selected_cells))

    # 0 - vertical, 1 - horizontal
    def cell_clicked(self, x, y, orientation):
        if not self.draw_in_progress:
            self.cell_clicked_guessing(x, y)
            return
        if len(self.current_ship) == 8:
            raise UserWarning('You can only use three cubits for a ship')
        ship_sz = self.ship_sizes[self.ship_num]
        if orientation == 0 and x + ship_sz > self.field_size or \
                orientation == 1 and y + ship_sz > self.field_size:
            raise UserWarning('You cannot place a ship with this orientation here')

        sz = len(self.current_ship)
        if sz >= 1 and (sz & (sz - 1)) == 0:
            if self.qbits_remaining == 0:
                raise UserWarning('You have no qubits left')
            self.qbits_remaining -= 1
            self.controller.change_qubits_left(self.qbits_remaining)

        xx, yy = x, y
        for i in range(ship_sz):
            self.controller.color_cell(xx, yy, self.ship_colors[self.ship_num])
            if orientation == 0:
                xx += 1
            else:
                yy += 1

        self.current_ship.append((x, y, orientation))

    def submit_guess(self):
        self.guesses += 1
        self.controller.change_guesses(self.guesses)
        print('Guess submitted')

        response = self.qgame.shoot_cells(self.selected_cells)
        for x, y, ship_id, health in response:
            if ship_id < 0:
                self.controller.color_cell(x, y, self.miss_color)
            elif health == 1:
                self.ships[ship_id].damage = 1
                self.controller.color_cell(x, y, self.injured_color)
            else:
                if health != 0:
                    print(f'Error: Ship ID > 0, health = {health}')
                self.ships[ship_id].damage = 0
                ship_coords_to_color = self._get_coords_to_color(x, y, ship_id)
                for x_, y_ in ship_coords_to_color:
                    self.controller.color_cell(x, y, self.killed_color)

    def _get_coords_to_color(self, x, y, ship_id):
        result = []
        flag = False
        for i, coords in enumerate(self.ships[ship_id].coordinates):
            fromx, fromy, hv = coords
            tox = fromx + 1 if hv == 0 else fromx + self.ships[ship_id].shape
            toy = fromy + 1 if hv == 1 else fromy + self.ships[ship_id].shape
            if fromx <= x < tox and fromy <= y < toy:
                if flag:
                    print('Error: one-ship copies intersection')
                flag = True
                for x_ in range(fromx, tox):
                    for y_ in range(fromy, toy):
                        result.append((x_, y_))
        if len(result) == 0:
            print('Error: no such points in specified ship')
        return result
