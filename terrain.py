from base import Shape
from definitions import terrain
import config
from shapely.geometry import LineString, MultiLineString, Point, MultiPoint

class TerrainBase(Shape):

    def __init__(self, shape, terrain_type=None):
        self._shape = shape
        #FIXME -- what is appropriate type?
        self._object = MultiPoint(self._shape)
        self._type = terrain_type

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, val):
        self._type = val


class BodyOfWater(TerrainBase):

    def __init__(self, shape):

        super().__init__(shape, terrain_type=terrain.water)

        self.set_display_repr(config.WATER_BLOCK)

    @property
    def shape(self):
        return self._object

    def __repr__(self):

        return str(self._path)


