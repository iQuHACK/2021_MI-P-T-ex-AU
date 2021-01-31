from tkinter import *
from tkinter.messagebox import showerror
from tkinter.ttk import *
import math
import game

FIELD_SIZE = 1000
N = 10
CELL_SIZE = FIELD_SIZE // N
FIELD_HIGHLIGHT = 2
assert (FIELD_SIZE % N == 0)


class Controller:
    @staticmethod
    def draw_next_ship(size: int, color: str, is_last: bool):
        current_ship.delete('all')
        if size > 0:
            center = CURRENT_SHIP_SIZE // 2
            CSZ = 50
            le = center - CSZ // 2
            ri = center + CSZ // 2
            up = center - CSZ * size // 2
            down = center + CSZ * size // 2
            for i in range(up, down + 1, CSZ):
                current_ship.create_line(le, i, ri, i)
            for i in range(size):
                current_ship.create_rectangle(le, up + i * CSZ, ri, up + (i + 1) * CSZ, fill=color)
            current_ship.create_line(le, up, le, down)
            current_ship.create_line(ri, up, ri, down)
        if is_last:
            next_ship.config(text='Finish')

    @staticmethod
    def color_cell(x, y, color):
        FH = FIELD_HIGHLIGHT
        field.create_rectangle(FH + y * CELL_SIZE, FH + x * CELL_SIZE, FH + (y + 1) * CELL_SIZE,
                               FH + (x + 1) * CELL_SIZE,
                               fill=color)

    @staticmethod
    def color_cell_guessing(x, y, color):
        FH = FIELD_HIGHLIGHT
        guessing_field.create_rectangle(FH + y * CELL_SIZE, FH + x * CELL_SIZE, FH + (y + 1) * CELL_SIZE,
                                        FH + (x + 1) * CELL_SIZE,
                                        fill=color)

    @staticmethod
    def change_qubits_left(cnt):
        qubits_left.config(text='Qubits left: ' + str(cnt))
        qubits_left.update()

    @staticmethod
    def change_guesses(cnt):
        guesses.config(text='Guesses: ' + str(cnt))
        guesses.update()

    @staticmethod
    def change_cells_left(cnt):
        cells_left.config(text='Cells left this guess: ' + str(cnt))
        cells_left.update()

    @staticmethod
    def init_guessing():
        init_guessing_field()


def cell_clicked(x, y, o):
    try:
        game.cell_clicked(x, y, o)
    except UserWarning as e:
        showerror(title='QBattleship', message=e.args[0])


def cell_clicked_lmb(event):
    cellx = math.floor(event.y // CELL_SIZE)
    celly = math.floor(event.x // CELL_SIZE)
    cell_clicked(cellx, celly, 0)


def cell_clicked_rmb(event):
    cellx = math.floor(event.y // CELL_SIZE)
    celly = math.floor(event.x // CELL_SIZE)
    cell_clicked(cellx, celly, 1)


def next_ship_clicked(event=None):
    try:
        game.next_ship_clicked()
    except UserWarning as e:
        showerror(title='QBattleship', message=e.args[0])


# creating main tkinter window/toplevel
master = Tk()
master.title('QBattleship')
master.resizable(False, False)

field = Canvas(master, width=FIELD_SIZE, height=FIELD_SIZE, highlightthickness=FIELD_HIGHLIGHT,
               highlightbackground='black')
field.bind('<Button-1>', cell_clicked_lmb)
field.bind('<Button-3>', cell_clicked_rmb)
master.bind('<space>', next_ship_clicked)
for i in range(9):
    FH = FIELD_HIGHLIGHT
    field.create_line(FH + CELL_SIZE * (i + 1), FH + 0, FH + CELL_SIZE * (i + 1), FH + FIELD_SIZE + 2)
    field.create_line(FH + 0, FH + CELL_SIZE * (i + 1), FH + FIELD_SIZE, FH + CELL_SIZE * (i + 1))

CURRENT_SHIP_SIZE = 300
current_ship = Canvas(master, width=CURRENT_SHIP_SIZE, height=CURRENT_SHIP_SIZE,
                      highlightthickness=2, highlightbackground='black')

qubits_left = Label(master, text='Qubits left: 11')
next_ship = Button(master, text='Next ship', command=next_ship_clicked)
field.pack(side=LEFT)
current_ship.pack(expand=False, anchor='n', padx=3, pady=3)
qubits_left.pack(anchor='n')
next_ship.pack(anchor='n')


def init_guessing_field():
    def submit_guess_clicked():
        game.submit_guess()

    master.withdraw()
    global guessing_field, guesses, cells_left
    master_guessing = Tk()
    master_guessing.title('QBattleship guessing')
    master_guessing.resizable(False, False)
    guessing_field = Canvas(master_guessing, width=FIELD_SIZE, height=FIELD_SIZE, highlightthickness=FIELD_HIGHLIGHT,
                            highlightbackground='black')
    guessing_field.bind('<Button-1>', cell_clicked_lmb)
    guessing_field.bind('<Button-3>', cell_clicked_rmb)
    for i in range(9):
        FH = FIELD_HIGHLIGHT
        guessing_field.create_line(FH + CELL_SIZE * (i + 1), FH + 0, FH + CELL_SIZE * (i + 1), FH + FIELD_SIZE + 2)
        guessing_field.create_line(FH + 0, FH + CELL_SIZE * (i + 1), FH + FIELD_SIZE, FH + CELL_SIZE * (i + 1))
    guessing_field.pack(side=LEFT)
    cells_left = Label(master_guessing, text='Cells left this guess: 5')
    cells_left.pack(anchor='ne')
    submit_guess = Button(master_guessing, text='Submit guess', command=submit_guess_clicked)
    submit_guess.pack(ancho='ne')
    guesses = Label(master_guessing, text='Guesses: 0')
    guesses.pack(anchor='ne')


game = game.GameField(Controller)

mainloop()
