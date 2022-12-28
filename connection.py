from enum import Enum
import numpy as np
import uuid
from shapely.geometry import LineString, MultiLineString
from base import Shape

import config

class connection_types(Enum):

    dirt_road = 1
    stone_road = 2
    asphalt_road = 3
    concrete_road = 4

class ConnectionBase:

    def __init__(self, source, dest, shape=None):

        self._source = source
        self._dest = dest
        self._shape = shape


    def set_shape(self, shape):
        self._shape = shape

    def get_length(self):
        return self._shape.length


class Road(Shape):

    def __init__(self, path, rtype):

        super().__init__()

        # FIXME -- need to check that path is 
        # continuous
        self._shape = None
        self._type = rtype
        self.add_path(path)
        # FIXME -- add id
        self._id = uuid.uuid4()
        self.set_display_repr(config.ROAD_DIRT_BLOCK)

    def __repr__(self):
        output = ''
        for g in self._shape.geoms:
            for coord in g.coords:
                output += str(coord)

        return output

    def get_id(self):
        return self._id

    def add_path(self, path):

        if path is None:
            raise ValueError

        x_diffs = np.diff([p[0] for p in path])
        y_diffs = np.diff([p[1] for p in path])

        if max(x_diffs+y_diffs) > 1 :
            print('Road is disconnected')
            return

        if len(set(path)) != len(path):
            print('Road has a self-intersect')
            return

        if self._object is None:
            self._object = MultiLineString([path])
        else:
            new_lines = [path] + [g for g in self._object.geoms]
            
            self._object= MultiLineString(new_lines)



def make_road_segment(start, end, rtype):

    if start[0] == end[0]:
        seg_start = min(start[1], end[1])
        seg_end = max(start[1], end[1])
        seq = np.arange(seg_start, seg_end)
        path = [(start[0], s) for s in seq]
        return Road(path, rtype)

    elif start[1] == end[1]:
        seg_start = min(start[0], end[0])
        seg_end = max(start[0], end[0])
        seq = np.arange(seg_start, seg_end)
        path = [(s, start[1]) for s in seq]
        return Road(path, rtype)
    
    else:
        raise ValueError('Road is not straight')



