import utils
import uuid
import config
from enum import Enum
from shapely.geometry import box
from base import Shape

import communication

#class zone_id:
#
#    self._zid = 0
#
#    @staticmethod
#    def id(self):
#        self._zid += 1
#        return self._zid

class zone_types(Enum):

    residential = 1
    commercial = 2
    industrial = 3
    farm = 4


class zone(Shape):

    def __init__(self, zone_types, shape):

        super().__init__(box(*shape))

        self._type = zone_types
        self._avalable_shape = self._object
        self._sites = []
        #FIXME -- add dynamic ID
        self._id = uuid.uuid4()
        # needs to
        self.set_display_repr(config.ZONE_BLOCK[self._type.name])

    def add_site_with_check(self, site):

        site_bounds = site.get_bounds()
        zone_bounds = self.get_bounds()

        if (site_bounds[0] < zone_bounds[0] or 
            site_bounds[1] < zone_bounds[1] or
            site_bounds[2] > zone_bounds[2] or
            site_bounds[3] > zone_bounds[3]):

            return False

        self._sites.append(site)

        return True

    def get_total_area(self):
        return self.get_area()

    def get_available_area(self):
        return self._avalable_shape.area

    def get_type(self):
        return self._type

    def get_id(self):
        return self._id

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

    def get_sites(self):
        return self._sites


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

    def _place_site(self, site):

        site_shape = site.get_shape()

        point = utils.generate_points_in_polygon(self._avalable_shape, 1)

        site.translate(point)

        if self._avalable_shape.contains(site_shape):
            self._avalable_shape = self._avalable_shape - site_shape
            self._sites.append(site)
        else:
            print ('WARNING -- could not place site')

    def update_connections(self, existing_sites):
        raise NotImplementedError

