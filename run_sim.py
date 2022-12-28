import sys

from base import board_area
from controller import Controller, AdvertBoard
from connection import Road, make_road_segment, connection_types
from components.zone import zone, zone_types
import config

import numpy as np

def main():

    road = make_road_segment((0, 50), (100, 50), connection_types.dirt_road)
    #road = make_road_segment((50, 0), (50, 100), connection_types.dirt_road)

    farm = zone(zone_types.farm, [0, 51, 20, 60])

    adv = AdvertBoard()

    play_area = board_area(0, 0, 100, 100)


    cont = Controller(play_area)
    cont.add_path(road)

    cont.add_empty_zone(farm)

    time = 0
    while True:
        time += 1
        print (time)

        cont.update_connections(adv)

        cont.immigrate()
        print (cont._sites)
        cont.display()


def calculate_attraction(board_area, controller):
    pass




if __name__ == '__main__':
    main()



