import utils
import uuid
import logging
import config
from shapely.geometry import box, Point, MultiPoint
from base import Shape
from definitions import zone_types

import communication

logger = logging.getLogger(__name__)

class Zone(Shape):

    def __init__(self, zone_types, shape):

        obj = None
        if isinstance(shape, tuple):
            obj = Point(shape)
        if isinstance(shape, list):
            if isinstance(list[0], tuple):
                obj = MultiPoint(shape)
            elif len(list) == 4:
                obj = box(*shape)
            else:
                logger.warning("Shape creation with given input not supported")
                logger.warning(shape)

        super().__init__(obj)

        self._type = zone_types
        self._avalable_shape = self._object
        self._sites = []
        #FIXME -- add dynamic ID
        self._id = uuid.uuid4()
        # needs to
        self.set_display_repr(config.ZONE_BLOCK[self._type.name])

    @property
    def type(self):
        return self._type

    @property
    def id(self):
        return self._id

    @property
    def sites(self):
        return self._sites

    def add_site_with_check(self, site):

        #site_bounds = site.get_bounds()
        #zone_bounds = self.get_bounds()

        #if (site_bounds[0] < zone_bounds[0] or 
        #    site_bounds[1] < zone_bounds[1] or
        #    site_bounds[2] > zone_bounds[2] or
        #    site_bounds[3] > zone_bounds[3]):

        #    return False

        #point = utils.generate_points_in_polygon(self._avalable_shape, 1)

        site_shape = site.shape

        if self.shape.contains(site_shape):
            overlaps_site = False
            for s in self._sites:
                if s.shape.contains(site_shape):
                    overlaps_site = True
                    break


            if not overlaps_site:
                self._sites.append(site)
                return True

        return False

    def get_total_area(self):
        return self.get_area()

    def get_sites_area(self):
        if not self._sites:
            return 0

        return sum([s.get_area() for s in self._sites])

    def get_available_area(self):
        return self._avalable_shape.get_area()

    def get_sites_coords(self):

        coords = []
        for s in self._sites:
            coords += s.get_coord_points()

        return coords


    def get_sites_needing_i(self):

        sites = []
        for s in self._sites:
            needed_i = s.get_needed_i_suppliers()
            if needed_i > 0:
                sites.append(s)
        return sites


    def get_sites_needing_c(self):

        sites = []
        for s in self._sites:
            needed_c = s.get_needed_c_suppliers()
            if needed_c > 0:
                sites.append(s)
        return sites

    def get_sites_with_remaining_capacity(self):

        sites = []
        for s in self._sites:
            open_slots = s.get_remaining_capacity()
            if open_slots > 0:
                sites.append(s)

        return sites

    def get_sites_with_open_applications(self):

        sites = []
        if not self._zone_type == zone_types.residential:
            return sites

        for s in self._sites:
            open_apps = s.get_open_applications()
            if open_apps > 0:
                sites.append(s)

        return sites



    def update_sites(self, global_parameters):

        if self._type == zone_types.residential:
            self._update_residential(global_parameters)
        elif self._type == zone_types.commercial:
            self._update_commercial(global_parameters)
        elif self._type == zone_types.industrial:
            self._update_industrial(global_parameters)


    def _update_residential(self, global_parameters):

        #FIXME should query for other paramters
        # and modify based on edu, etc
        n_jobs = global_parameters['open_jobs']

        total_prob = n_jobs * config.JOBS_MULTIPLIER

        n_sites = np.random.poisson(total_prob)

        for _ in range(0, n_sites):
            # FIXME -- pass edu etc
            self._create_housing()

    def _create_housing(self):

        # FIXME -- should allow larger housing
        n_residents = np.random.poisson(1)+1

        shape = np.random.choice(config.site_shapes) 

        # FIXME -- adjust with bigger housing
        new_site = housing(n_residents, shape)
        new_site.add_residents(n_residents)

        self._place_site(new_site)

    def _update_commercial(self, global_parameters):

        #FIXME should query for other paramters
        # and modify based on edu, etc
        n_consumers = global_parameters['population']
        n_suppliers = global_parameters['industry_capacity']

        total_prob = (
            n_consumers * CONSUMERS_MULTIPLIER
          + n_suppliers * SUPPLIERS_MULTIPLIER
        )
        n_sites = np.random.poisson(total_prob)

        for _ in range(0, n_sites):
            # FIXME -- pass edu etc
            self._create_commercial(n_consumers)

    def _create_commercial(self, total_consumers):

        n_jobs = np.random.poisson(1) + 1

        mean_consumers = total_consumers * CONSUMERS_MULTIPLIER

        n_capacity = np.random.poisson(mean_consumers) + 1

        n_suppliers = np.random.poisson(2) + 1

        shape = np.random.choice(config.site_shapes) 

        new_site = business(zone_types.commercial, n_jobs, n_capacity, n_suppliers, shape)

        self._place_site(new_site)

    def _update_industrial(self, global_parameters):

        #FIXME should query for other paramters
        # and modify based on edu, etc
        n_consumers = global_parameters['commercial_output']
        n_suppliers = global_parameters['commerical_capacity']

        total_prob = (
            n_consumers * CONSUMERS_MULTIPLIER
          + n_suppliers * SUPPLIERS_MULTIPLIER
        )
        n_sites = np.random.poisson(total_prob)

        for _ in range(0, n_sites):
            # FIXME -- pass edu etc
            self._create_industrial(n_consumers)

    def _create_industrial(self, total_consumers):

        n_jobs = np.random.poisson(1) + 1

        mean_consumers = total_consumers * CONSUMERS_MULTIPLIER

        n_capacity = np.random.poisson(mean_consumers) + 1

        n_suppliers = np.random.poisson(2) + 1

        shape = np.random.choice(config.site_shapes) 

        new_site = business(zone_types.industrial, n_jobs, n_capacity, n_suppliers, shape)

        self._place_site(new_site)

    def update_connections(self, existing_sites):
        raise NotImplementedError

