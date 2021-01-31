from quantum_logic import *


HORIZ = 0
VERT = 1
DEFSHOOTS = 5


def main():
    f = open("ships2.txt", 'r')
    line = f.readline()
    shoots, size = line.split(' ')
    lines = f.readline()
    sets = lines.split(', ')
    sets_from_ships = []
    for i in sets:
        sets_from_ships.append([int(j) for j in i.split(' ')])

    ships = []
    for line in f:
        params = line.split(' ')
        coords = []
        for i in range((len(params) - 1) // 3):
            coords.append((int(params[3*i+1]), int(params[3*i+2]), int(params[3*i+3])))
        ships.append(Battleship(int(params[0]), coords))
        print(ships[-1].coordinates, ships[-1].shape)
    f.close()
    game = QuantumGame(ships, int(shoots), int(size))
    result = game.qubit_sets_from_ships()
    print(lines)
    for i in result:
        print(i.ship_ids, i.intersection_ids)
    test_simple_case()


# [[   0 -100 -100 -100 -100 -100]
#  [   0    0 -100    0 -100 -100]
#  [-100 -100 -100    0    0 -100]
#  [-100    1 -100 -100 -100 -100]
#  [-100 -100 -100 -100 -100 -100]
#  [-100 -100 -100 -100 -100 -100]]
def test_simple_case():
    ships = [
        Battleship(shape=2, coordinates=[(0, 0, HORIZ), (1, 3, HORIZ)]),
        Battleship(shape=2, coordinates=[(1, 0, VERT), (2, 3, VERT)]),
        Battleship(shape=1, coordinates=[(3, 1, VERT)])
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
#  [-100    4    4    4 -100    5 -100 -100 -100 -100 -100]
#  [-100 -100 -100 -100 -100    5 -100 -100    4 -100 -100]
#  [-100 -100 -100 -100 -100 -100 -100 -100    4 -100 -100]
#  [-100 -100 -100 -100 -100 -100    4 -100 -100 -100 -100]
#  [-100    4 -100 -100    4    4    4 -100 -100 -100 -100]
#  [-100    4 -100 -100 -100 -100 -100 -100    1 -100 -100]
#  [-100    4 -100 -100 -100 -100 -100 -100 -100 -100 -100]
#  [-100    4    4    4 -100 -100    5    5 -100 -100 -100]
#  [-100 -100 -100 -100 -100 -100 -100 -100 -100 -100 -100]
#  [-100 -100 -100 -100 -100 -100 -100 -100 -100 -100 -100]]

# [(1, 1, 1), (5, 4, 1), (8, 1, 1)] 3
# [(6, 8, 1)] 1
# [(5, 1, 0)] 4
# [(8, 7, 0)] 1
# [(2, 8, 0), (4, 6, 0)] 2
# [(1, 5, 0), (8, 6, 1)] 2
def test_big_field():
    pass


if __name__ == '__main__':
    main()
