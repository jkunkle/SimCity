from shapely.geometry import Polygon, LineString, MultiLineString, box
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

    def get_mask(self):
        xmax = self._object.bounds[2]+1
        ymax = self._object.bounds[3]+1

        mask = np.zeros([int(xmax), int(ymax)])

        for ix, iy in self.iter_points():
            mask[ix, iy] = 1

        return mask

    def get_shape(self):
        return self._object

    def get_bounds(self):
        return self._object.bounds

    def get_xmax(self):
        return int(self._object.bounds[2])
    def get_ymax(self):
        return int(self._object.bounds[3])

    def get_xmin(self):
        return int(self._object.bounds[0])
    def get_ymin(self):
        return int(self._object.bounds[1])

    def iter_points(self):

        if self._object is None:
            # FIXME -- better error?
            raise ValueError('Shape object is not instantiated!')

        end_add = 0
        if isinstance(self._object, LineString):
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
        return self._object.area

class board_area(Shape):

    def __init__(self, x=None, y=None, x_span=None, y_span=None):

        super().__init__(box(x, y, x_span, y_span))

        self.set_display_repr(config.EMPTY_BLOCK)

        self._x = x
        self._y = y
        self._x_span = x_span
        self._y_span = y_span

    def get_xy(self):
       return (self._x, self._y)

    def get_x_span(self):
        return self._x_span
    def get_y_span(self):
        return self._y_span

    def get_area(self):
        return self.get_x_span()*self.get_y_span()

