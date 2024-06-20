from terrain import BodyOfWater
import numpy as np
import random
from shapely.geometry import Point

def generate_river(play_area):

    path = []
    seed_path = []
    # choose a direction
    direction = np.array([1, 0])

    # choose a starting location
    start = (0, 30)

    seed_path.append(np.array(start))

    while True:
        bump_scale = random.uniform(-1, 1)

        perp_bump = np.array([bump_scale*direction[1], -1*bump_scale*direction[0]])


        new_vector = direction + perp_bump

        new_perp = np.array([new_vector[1], -1*new_vector[0]])

        last_loc = seed_path[-1]
        new_loc = last_loc + new_vector

        seed_path.append(new_loc)
        path.append(new_loc)
        for i in range(-2, 3):

            new_element = new_loc + (new_perp*i)
            if play_area.shape.contains(Point(new_element[0], new_element[1])):
                path.append(new_element)

        if not play_area.shape.contains(Point(new_loc[0], new_loc[1])):
            break

    path = [(int(x[0]), int(x[1])) for x in path]
    path = list(set(path))
    # FIXME -- improve if performance is needed
    nadd = None
    while nadd is None or nadd > 0:
        nadd = 0
        for x in range(0, play_area.x_span):
            for y in range(0, play_area.y_span):

                if (x, y) not in path:
                    left = (x-1, y)
                    right = (x+1, y)
                    up = (x, y+1)
                    down = (x, y-1)

                    n_adj = 0
                    n_adj += int(left in path or x == 0)
                    n_adj += int(right in path or x == play_area.x_span)
                    n_adj += int(up in path or y == 0)
                    n_adj += int(down in path or y == play_area.y_span)

                    if n_adj >= 3:
                        path.append((x,y))
                        nadd += 1

    bow = BodyOfWater(path)

    return bow

