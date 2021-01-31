from quantum_logic import *


HORIZ = 0
VERT = 1
DEFSHOOTS = 5


def main():
    test_simple_case()
    test_big_field()
    test_by_sergey()
    # print('Everything is OK!')


# [[   0 -100 -100 -100 -100 -100]
#  [   0    0 -100    0 -100 -100]
#  [-100 -100 -100    0    0 -100]
#  [-100    1 -100 -100 -100 -100]
#  [-100 -100 -100 -100 -100 -100]
#  [-100 -100 -100 -100 -100 -100]]
def test_simple_case():
    ships = [
        Battleship(shape=2, coordinates=[(0, 0, VERT), (1, 3, VERT)]),
        Battleship(shape=2, coordinates=[(1, 0, HORIZ), (2, 3, HORIZ)]),
        Battleship(shape=1, coordinates=[(3, 1, HORIZ)])
    ]
    qgame = QuantumGame(ships=ships, field_size=5, default_shoots_number=3)
    shots = [(0, 3), (1, 0), (2, 2)]
    result = qgame.shoot_cells(shots)
    print(result)


# [[-100 -100 -100 -100 -100 -100 -100 -100 -100 -100 -100]
#  [-100    0    0    0 -100    2 -100 -100 -100 -100 -100]
#  [-100 -100 -100 -100 -100    2 -100 -100    0 -100 -100]
#  [-100 -100 -100 -100 -100 -100 -100 -100    0 -100 -100]
#  [-100 -100 -100 -100 -100 -100    0 -100 -100 -100 -100]
#  [-100    0 -100 -100    0    0    0 -100 -100 -100 -100]
#  [-100    0 -100 -100 -100 -100 -100 -100    1 -100 -100]
#  [-100    0 -100 -100 -100 -100 -100 -100 -100 -100 -100]
#  [-100    0    0    0 -100 -100    2    2 -100 -100 -100]
#  [-100 -100 -100 -100 -100 -100 -100 -100 -100 -100 -100]
#  [-100 -100 -100 -100 -100 -100 -100 -100 -100 -100 -100]]
def test_big_field():
    ships = [
        Battleship(shape=3, coordinates=[(1, 1, HORIZ), (5, 4, HORIZ), (8, 1, HORIZ)]),
        Battleship(shape=1, coordinates=[(6, 8, HORIZ)]),
        Battleship(shape=4, coordinates=[(5, 1, VERT)]),
        Battleship(shape=1, coordinates=[(8, 7, VERT)]),
        Battleship(shape=2, coordinates=[(2, 8, VERT), (4, 6, VERT)]),
        Battleship(shape=2, coordinates=[(1, 5, VERT), (8, 6, HORIZ)]),
    ]
    shots = [(1, 1), (6, 8), (3, 3), (8, 1), (8, 7)]
    qgame = QuantumGame(ships=ships, field_size=10, default_shoots_number=DEFSHOOTS)
    result = qgame.shoot_cells(shots)
    print(result)


def test_by_sergey():
    ships = [
        Battleship(shape=1, coordinates=[(1, 1, HORIZ), (5, 4, HORIZ)]),
        Battleship(shape=1, coordinates=[(3, 1, HORIZ)])
    ]
    shots = [(5, 4), (3, 1), (8, 8)]
    qgame = QuantumGame(ships=ships, field_size=10, default_shoots_number=3)
    result = qgame.shoot_cells(shots)
    print(result)


if __name__ == '__main__':
    main()
