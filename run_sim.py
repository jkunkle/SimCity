import sys
import random
from shapely.geometry import Point

from base import board_area
from controller import Controller, AdvertBoard
from connection import Road, make_road_segment, connection_types
from components.zone import zone, zone_types
from definitions import resource
import generators as gen
import config


import numpy as np

def main():

    road = make_road_segment((0, 50), (100, 50), connection_types.dirt_road)
    #road = make_road_segment((50, 0), (50, 100), connection_types.dirt_road)

    farm = zone(zone_types.farm, [0, 51, 20, 60])

    play_area = board_area(0, 0, 100, 100)

    cont = Controller(play_area)
    cont.add_path(road)
    river = gen.generate_river(play_area)
    cont.add_resource(resource.water, river)

    cont.add_empty_zone(farm)

    time = 0
    while True:
        time += 1
        print (time)

        cont.run_step()

        cont.display()





def calculate_attraction(board_area, controller):
    pass




if __name__ == '__main__':
    main()



