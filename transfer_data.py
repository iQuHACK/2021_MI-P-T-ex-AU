from quantum_logic import *


def get_ships(string):
    ships = []
    first = string.split(', ')
    for i in first:
        coords = []
        shape, sets = i.split('. ')
        shape = int(shape)
        coordinates = sets.split('; ')
        for j in coordinates:
            tup = [int(k) for k in j.split(' ')]
            coords.append(tuple(tup))
        ships.append(Battleship(shape, coords))
    return ships


def get_shot(string):
    length, shots = string.split(';')
    length = int(length)
    shots = shots.split(' ')
    shoots = []
    for i in shots:
        shoots.append([int(i.split('.')[0]), int(i.split('.')[1])])
    return shoots


def send_shots_results(shoots):
    send_buf = ''
    for i in shoots:
        for j in i:
            send_buf += str(j) + ' '
        send_buf = send_buf[:-1] + ', '
    return send_buf[:-2].encode()


def send_ships(ships):
    send_buf = ""
    for i in ships:
        line = str(i.shape) + '. '
        for j in i.coordinates:
            line += str(j[0]) + ' ' + str(j[1]) + ' ' + str(j[2]) + '; '
        send_buf += line[:-2] + ', '
        send_buf = send_buf[:-2].encode()
    return send_buf


def send_shots(shots):
    send_buf = str(len(shots)) + ';'
    for i in shots:
        send_buf += str(i[0]) + '.' + str(i[1]) + ' '
    return send_buf[:-1].encode()


def get_shots_result(string):
    shoots = string.split(', ')
    shots = []
    for i in shoots:
        tmp = []
        for j in i.split(' '):
            tmp.append(int(j))
    shots.append(tmp)
    return shots
