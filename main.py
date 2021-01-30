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


def color_cell(x, y, color):
    FH = FIELD_HIGHLIGHT
    field.create_rectangle(FH + y * CELL_SIZE, FH + x * CELL_SIZE, FH + (y + 1) * CELL_SIZE, FH + (x + 1) * CELL_SIZE,
                           fill=color)


def change_qubits_left(cnt):
    qubits_left.config(text='Qubits left: ' + str(cnt))


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
field.pack(side=LEFT, padx=3, pady=3)
current_ship.pack(expand=False, anchor='n', padx=3, pady=3)
qubits_left.pack(anchor='n')
next_ship.pack(anchor='n')

game = game.GameField(draw_next_ship, color_cell, change_qubits_left)

mainloop()
