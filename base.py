from shapely.geometry import Polygon, LineString, MultiLineString, Point, MultiPoint
import numpy as np
import config

class Shape:

    def __init__(self, obj=None):
        #FIXME -- consider adding addtl info storage
        self._object = obj
        self._display_repr = None

    def set_display_repr(self, drepr):
        self._display_repr = drepr
    def get_display_repr(self):
        return self._display_repr

    def update_shape(self, other):

        if isinstance(self._object, Point):
            if isinstance(other, Point):
                self._object = MultiPoint([self._object, other])
            else:
                raise ValueError('Only supported to add point to point')
        elif isinstance(self._object, MultiPoint):
            if isinstance(other, Point):
                self._object = MultiPoint(list(self._object.geoms) + [other])
            if isinstance(other, MultiPoint):
                self._object = MultiPoint(self._object.geoms + other.geoms)
        else:
            raise ValueError('Only supported to update this type of object')

    def get_mask(self):
        xmax = self._object.bounds[2]+1
        ymax = self._object.bounds[3]+1

        mask = np.zeros([int(xmax), int(ymax)])

        for ix, iy in self.iter_points():
            mask[ix, iy] = 1

        return mask

    @property
    def shape(self):
        return self._object

    def get_bounds(self):
        return self._object.bounds

    def xmax(self):
        return int(self._object.bounds[2])
    def ymax(self):
        return int(self._object.bounds[3])

    def xmin(self):
        return int(self._object.bounds[0])
    def ymin(self):
        return int(self._object.bounds[1])

    def contains(self, point):
        if not isinstance(point, Point):
            point = Point(point)
        return self._object.contains(point)


    def iter_points(self):

        if self._object is None:
            # FIXME -- better error?
            raise ValueError('Shape object is not instantiated!')

        end_add = 0
        if isinstance(self._object, Point):
            yield (self._object.x, self._object.y)

        elif isinstance(self._object, MultiPoint):
            for pt in self._object.geoms:
                yield (pt.x, pt.y)

        elif isinstance(self._object, LineString):
            for c in self._object.coords:
                yield c

        elif isinstance(self._object, MultiLineString):
            for line in self._object.geoms:
                for c in line.coords:
                    yield tuple([int(x) for x in c])

        else:
            bounds = self._object.bounds
            x0 = int(bounds[0])
            y0 = int(bounds[1])
            x1 = int(bounds[2])
            y1 = int(bounds[3])

            for ix in range(x0, x1+end_add):
                for iy in range(y0, y1+end_add):
                    yield (ix, iy)

    def get_area(self):
        if self._object is None:
            # FIXME -- better error?
            raise ValueError('Shape object is not instantiated!')
        if isinstance(self._object, Point):
            return 1
        elif isinstance(self._object, MultiPoint):
            return len(self._object.geoms)
        else:
            return self._object.area

