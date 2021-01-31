from quantum_logic import *
from transfer_data import *

f = open("ships.txt", 'r')
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
    for i in range((len(params) - 1)// 3):
        coords.append((int(params[3*i+1]), int(params[3*i+2]), int(params[3*i+3])))
    ships.append(Battleship(int(params[0]), coords))
    print(ships[-1].coordinates, ships[-1].shape)
f.close()
game = QuantumGame(ships, int(shoots), int(size))
result = send_ships(game.ships)
result = result.decode()
ships = get_ships(result)
print(result)
for i in ships:
    print(i.coordinates, i.shape)

shoots = [[1, 1, 2, 1], [2, 5, 4, 1], [4, 2, 1, 0], [5, 7, 9, 1]]
print(shoots)
test = send_shots_results(shoots).decode()
print(test)
print(get_shots_result(test))


