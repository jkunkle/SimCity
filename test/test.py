import unittest

from shapely.geometry import Polygon, LineString, MultiLineString, box, Point, MultiPoint
from base import board_area, Shape
from controller import Controller
from components.zone import zone, zone_types

class TestShape(unittest.TestCase):

    def test_create_shape(self):
        sh = Shape()
        assert sh._object == None

    def test_shape_point(self):

        sh = Shape(Point(0, 0))
        print (sh.get_area())




class TestZone(unittest.TestCase):

    def test_create_zone(self):
        test = zone(zone_types.farm, [0, 0, 0, 0])



class TestController(unittest.TestCase):

    def test_controller_zone(self):

        play_area = board_area(0, 0, 100, 100)
        cont = Controller(play_area)
        farm = zone(zone_types.farm, [0, 51, 20, 60])
        cont.add_empty_zone(farm)

        cont.run_step()
        

    def test_controller_point_zone(self):

        play_area = board_area(0, 0, 100, 100)
        cont = Controller(play_area)
        farm = zone(zone_types.farm, [0, 0, 0, 0])
        cont.add_empty_zone(farm)

        cont.run_step()
        cont.run_step()
        



if __name__ == '__main__':
    unittest.main()

