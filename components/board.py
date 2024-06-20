from shapely.geometry import box, Point
from base import Shape
from definitions import zone_types
from components.zone import Zone
import config

class Board(Shape):

    def __init__(self, x=None, y=None, x_span=None, y_span=None):

        super().__init__(box(x, y, x_span, y_span))

        self.set_display_repr(config.EMPTY_BLOCK)

        self._x = x
        self._y = y
        self._x_span = x_span
        self._y_span = y_span

        self._zones = []
        self._paths = []
        self._terrain = []
        self._elevation = []

    @property
    def paths(self):
        return self._paths

    def add_path(self, path):
        self._paths.append(path)

    @property
    def terrain(self):
        return self._terrain

    def add_terrain(self, terr):
        self._terrain.append(terr)

    def get_terrain_shape(self, ttype):
        
        matches = [t for t in self._terrain if t.type == ttype]

        if not matches:
            return None

        if len(matches) == 1:
            return matches[0].shape

        raise NotImplementedError('Should return a MultiSomething')

    def get_terrain_type(self, x, y):

        terr_type = config.DEFAULT_TERRAIN_TYPE
        for ter in self.terrain:
            if ter.contains(x, y):
                terr_type = ter.type

        return terr_type

    @property
    def x_span(self):
        return self._x_span

    @property
    def y_span(self):
        return self._y_span

    def get_xy(self):
       return (self._x, self._y)

    def get_area(self):
        return (self.x_span - self._x)*(self.y_span - self._y)

    def is_valid(self, x, y):
        if x < self._x :
            return False
        if y < self._y :
            return False
        if x > self._x + self.x_span :
            return False
        if y > self._y + self.y_span :
            return False

        return True

    def get_zones(self, ztype=None, zone_id=None):

        if zone_id is not None:
            match_zones = [z for z in self._zones if z.id == zone_id]
            if len(match_zones) == 0:
                print ('Failed to find zone with ID, ', zone_id)
                return None
            if len(match_zones) > 1:
                print ('Multiple zones foud with ID, ', zone_id)
                return None

            return match_zones[0]

        if ztype is not None:
            return [z for z in self._zones if z.type == ztype]

        return self._zones

    def get_i_zones(self):
        return self.get_zones(ztype=zone_types.industrial)

    def get_c_zones(self):
        return self.get_zones(ztype=zone_types.commercial)

    def get_r_zones(self):
        return self.get_zones(ztype=zone_types.residential)

    def get_f_zones(self):
        return self.get_zones(ztype=zone_types.farm)

    def get_zone_density(self):

        result = {}
        for z in self._zones:
            tp = z.type


            den = z.get_total_area()
            num = z.get_sites_area()

            result.setdefault(tp, []).append((num, den))

        density = {}
        for tp, vals in result.items():
            try:
                density[tp] = sum([v[0] for v in vals])/sum([v[1] for v in vals])
            except ZeroDivisionError:
                density[tp] = None

        return density

    def get_residents(self):

        for z in self.get_zones():
            for s in z.sites:
                for r in s.residents:
                    yield r

            
    def add_empty_zone(self, zone):
        self._zones.append(zone)

    def add_zone(self, points, zone_type):

        if not isinstance(points, list):
            points = [points]

        if self._has_conflict(points, zone_type):
            return 0

        for p in points:
            self.add_zone_point(p, zone_type)

    def add_zone_point(self, point_coords, zone_type):

        curr_zones = list(filter(lambda x: x.type == zone_type, self._zones))

        if not curr_zones:
            self.add_empty_zone(Zone(zone_type, point_coords))
        else:
            point = Point(point_coords)
            distances = [x.shape.distance(point) for x in curr_zones]

            min_dist = min(distances)

            if min_dist <= 1:
                min_idx = distances.index(min_dist)

                curr_zones[min_idx].update_shape(point)

            else:
                self.add_empty_zone(Zone(zone_type, point_coords))

    def _has_conflict(self, points, zone_type):

        build_eff_all = config.TERRAIN_BUILD_EFFICIENCY[zone_type]

        for ter in self.terrain:
            build_eff = build_eff_all[ter.type]
            if build_eff == 0:
                for p in points:
                    if ter.contains(p):
                        return 1

        return 0

