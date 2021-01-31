def draw_ids_on_ships(field, ships, idx):
    for i, qship in enumerate(ships):
        for shipcoords in qship.coordinates:
            x, y, hv = shipcoords
            tox = x + 1 if hv == 0 else x + qship.shape
            toy = y + 1 if hv == 1 else y + qship.shape
            tox = min(tox, len(field))
            toy = min(toy, len(field[0]))
            for x_ in range(x, tox):
                for y_ in range(y, toy):
                    field[x_][y_] = idx
    return field
