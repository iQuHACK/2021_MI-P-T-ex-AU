from quantum_logic import *

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
f.close()
game = QuantumGame(ships, int(shoots), int(size))
result = game.qubit_sets_from_ships()
print(lines)
for i in result:
    print(i.ship_ids, end=', ')

