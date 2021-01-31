from quantum_logic import *


HORIZ = 0
VERT = 1
DEFSHOOTS = 5


def main():
    test_simple_case()
    test_big_field()
    print('Everything is OK!')


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
    expected_result = [
        QubitSet(idx=0, ship_ids=[0, 1], intersection_ids=[((0, 0), (1, 0)), ((0, 1), (1, 1))], nqubits=2),
        QubitSet(idx=1, ship_ids=[2], intersection_ids=[], nqubits=0)
    ]
    qgame = QuantumGame(ships=ships, field_size=5, default_shoots_number=DEFSHOOTS)
    result = qgame.qubit_sets_from_ships()
    result = sorted(result, key=lambda x: sorted(x.ship_ids))
    assert result == expected_result


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
    expected_result = [
        QubitSet(idx=0, ship_ids=[0, 2, 4], intersection_ids=[((0, 1), (4, 1)), ((0, 2), (2, 0))], nqubits=3),
        QubitSet(idx=1, ship_ids=[1], intersection_ids=[], nqubits=0),
        QubitSet(idx=2, ship_ids=[3, 5], intersection_ids=[((3, 0), (5, 1))], nqubits=1)
    ]
    qgame = QuantumGame(ships=ships, field_size=10, default_shoots_number=DEFSHOOTS)
    result = qgame.qubit_sets_from_ships()
    result = sorted(result, key=lambda x: sorted(x.ship_ids))
    assert result == expected_result


if __name__ == '__main__':
    main()
