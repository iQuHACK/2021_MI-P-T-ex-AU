from tkinter import *
from tkinter.ttk import *
import math

FIELD_SIZE = 1000
N = 10
CELL_SIZE = FIELD_SIZE // N
FIELD_HIGHLIGHT = 2
assert (FIELD_SIZE % N == 0)


def draw_next_ship(size):
    current_ship.delete('all')
    center = CURRENT_SHIP_SIZE // 2
    CSZ = 50
    le = center - CSZ // 2
    ri = center + CSZ // 2
    up = center - CSZ * size // 2
    down = center + CSZ * size // 2
    for i in range(up, down + 1, CSZ):
        current_ship.create_line(le, i, ri, i)
    for i in range(size):
        current_ship.create_rectangle(le, up + i * CSZ, ri, up + (i + 1) * CSZ, fill='lawn green')
    current_ship.create_line(le, up, le, down)
    current_ship.create_line(ri, up, ri, down)


def color_cell(x, y, color):
    FH = FIELD_HIGHLIGHT
    field.create_rectangle(FH + y * CELL_SIZE, FH + x * CELL_SIZE, FH + (y + 1) * CELL_SIZE, FH + (x + 1) * CELL_SIZE, fill=color)


def cell_clicked(x, y, orientation):
    pass


def next_ship_clicked():
    pass


def cell_clicked_lmb(event):
    cellx = math.floor(event.y // CELL_SIZE)
    celly = math.floor(event.x // CELL_SIZE)
    color_cell(cellx, celly, 'red')


def cell_clicked_rmb(event):
    cellx = math.floor(event.y // CELL_SIZE)
    celly = math.floor(event.x // CELL_SIZE)
    color_cell(cellx, celly, 'lawn green')


# creating main tkinter window/toplevel
master = Tk()
master.title('QBattleship')

field = Canvas(master, width=FIELD_SIZE, height=FIELD_SIZE, highlightthickness=FIELD_HIGHLIGHT, highlightbackground='black')
field.bind('<Button-1>', cell_clicked_lmb)
field.bind('<Button-3>', cell_clicked_rmb)
for i in range(9):
    FH = FIELD_HIGHLIGHT
    field.create_line(FH + CELL_SIZE * (i + 1), FH + 0, FH + CELL_SIZE * (i + 1), FH + FIELD_SIZE + 2)
    field.create_line(FH + 0, FH + CELL_SIZE * (i + 1), FH + FIELD_SIZE, FH + CELL_SIZE * (i + 1))

CURRENT_SHIP_SIZE = 300
current_ship = Canvas(master, width=CURRENT_SHIP_SIZE, height=CURRENT_SHIP_SIZE,
                      highlightthickness=2, highlightbackground='black')
field.pack(side=LEFT, padx=3, pady=3)
current_ship.pack(side=RIGHT, expand=False, anchor='n', padx=3, pady=3)
draw_next_ship(3)
draw_next_ship(2)

mainloop()
