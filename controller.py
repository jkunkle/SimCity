from definitions import zone_types
from components.farm import Farm
from components.resident import Resident
import random
import utils
import pandas as pd
import numpy as np
import logging
import PySimpleGUI as sg
from shapely.geometry import Point
from shapely import affinity
from scipy.stats import poisson

from pathfinder import PathFinder

import config

logger = logging.getLogger(__name__)

class AdvertBoard:

    def __init__(self):

        self._adverts = []

    def post_advert(self, adv):
        self._adverts.append(adv)

    def get_job_adverts(self):
        return [a for a in self._adverts if a.is_job_advert()]

    def get_slot_adverts(self):
        return [a for a in self._adverts if a.is_slot_advert()]


class Controller():

    def __init__(self, board):

        self._export_rate = 0.1
        self._applications = []
        self._adv_bd = AdvertBoard()
        self._time = 0
        self._board = board
        self._path_finder = PathFinder(board)

    @property
    def board(self):
        return self._board


    #def add_path(self, path):

    #    # FIXME -- if new path is of same type and adjacent
    #    # then append to that object rather than list of paths
    #    #related_paths = filter(lambda x: x.get_type() == path.get_type(), self._paths)
    #    self.board.add_path(path)

    #def add_resource(self, res_type, shape):
    #    self._resources.append(shape)

    #def get_resources(self):
    #    return self._resources

    def _collect_openings(self):

        all_openings = {}
        for zone in self._zones:
            zone.collect_openings(all_openings)

        return all_openings

    def get_time(self):
        return self._time

    def run_step(self):
        self._time += 1

        #if time % 100 == 0:
        #    self.update_connections()

        for r in self.board.get_residents():
            r.increment(1)

        self.immigrate()


    def update_connections(self):

        self._generate_applications(self._adv_bd)
        self._generate_new_adverts(self._adv_bd)
        needed_i_sites = self._get_sites_needing_i()
        existing_i_sites = self._get_i_sites_with_slots()

        self._match_sites(existing_i_sites, needed_i_sites)

        needed_c_sites = self._get_sites_needing_c()
        existing_c_sites = self._get_c_sites_with_slots()

        self._match_sites(existing_c_sites, needed_c_sites)

        needed_r_sites = self._get_sites_needing_jobs()
        existing_r_sites = self._get_open_applicants()

        self._match_sites(existing_r_sites, needed_r_sites)

        for s in self._sites:
            for r in s.get_residents():
                r.update_connections()

    def _match_sites(self, existing, needed):

        for ex in existing:
            match_need = None
            best_score = 0
            for n in needed:
                score = self._calculate_match(ex, n)
                if score > best_score:
                    match_need = n
                    best_score = score

            ex.add_connection(match_need)

    def _generate_applications(self, board):

        for s in self._sites:

            if s.get_zone_type() == zone_types.residential:
                continue

            s.generate_applications(board)

    def _generate_new_adverts(self, board):

        for s in self._sites:

            if s.get_zone_type() == zone_types.residential:
                continue

            s.generate_adverts(board)


    def _get_sites_needing_i(self):

        sites = []
        for z in self.board.get_i_zones():
            sites += z.get_sites_needing_i()
        for z in self.board.get_c_zones():
            sites += z.get_sites_needing_i()

        return sites

    def _get_sites_needing_c(self):

        sites = []
        for z in self.board.get_i_zones():
            sites += z.get_sites_needing_c()
        for z in self.board.get_c_zones():
            sites += z.get_sites_needing_c()
        for z in self.board.get_r_zones():
            sites += z.get_sites_needing_c()

    def _get_sites_needing_jobs(self):

        sites = []
        for z in self.board.get_c_zones():
            sites.append(z.get_sites_with_remaining_capacity())
        for z in self.board.get_i_zones():
            sites.append(z.get_sites_with_remaining_capacity())

        return sites


    def _get_open_applicants(self):

        sites = []
        for z in self.board.get_r_zones():
            sites += z.get_sites_with_open_applications()

        return sites

    def _get_i_sites_with_slots(self):

        sites = []
        for z in self.board.get_i_zones():
            sites += z.get_sites_with_remaining_capacity()

        return sites
        
    def _get_c_sites_with_slots(self):

        sites = []
        for z in self.board.get_c_zones():
            sites += z.get_sites_with_remaining_capacity()

        return sites
        

    def update_sites(self):
        get_open_jobs()
        get_population()
        get_commercial_capacity()
        get_commercial_output()
        get_industrial_capacity()

        for zone in self.board.get_zones():
            zone.update_sites(self._parameters)


    def display(self):
        
        display_items = [self.get_shape()]
        display_items += self._resources
        display_items += self._paths
        display_items += self._zones
        display_items += self._sites

        layout = []
        x_span = self.get_shape().get_x_span()
        y_span = self.get_shape().get_y_span()

        comb_mask = None
        values = {0 : ' '}
        for iobj, obj in enumerate(display_items):

            mask = obj.get_mask()

            xmax = obj.xmax()
            ymax = obj.ymax()

            pad_x = x_span - xmax
            pad_y = y_span - ymax
            if pad_x < 0 or pad_y < 0:
                raise ValueError("Object %s exceeds board boundary" %obj)

            mask = np.pad(mask, [(0, pad_x), (0, pad_y)])

            mask[mask == 1] = iobj+1
            values[iobj+1] = obj.get_display_repr()
            
            if comb_mask is None:
                comb_mask = mask
            else:
                comb_mask = np.maximum(comb_mask, mask)

        
        comb_rows = comb_mask.transpose().tolist()

        for row in comb_rows:
            print (''.join([values[int(x)] for x in row]))

    def immigrate(self):

        # FIXME may want to schedule multiple
        # calculators to determine immigration
        zone_density = self.board.get_zone_density()

        immi_zones = self._get_immigration_by_zone_type(zone_density)
        # determine immigration for each zone type
        for tp, n_immi in immi_zones.items():

            if n_immi > 0:
                logger.debug('immigrate %d', n_immi)

            for iimmi in range(0, n_immi):
                all_type_zones = self.board.get_zones(tp)

                new_site = None
                while new_site is None:
                    # FIXME -- shape shoud depend on purchase price
                    shape = random.choice(config.site_shapes)
    
                    best_site = self.find_best_site(tp)
                    if best_site is None:
                        break

                    try:
                        new_site = self._generate_site(tp, shape, best_site)
                    except RuntimeError:
                        new_site = None
                        break

                if new_site is None:
                    continue

                print ('Generated site')
                print (new_site)
                # FIXME -- do we need additional info to 
                # generate occupant?
                resident = self._generate_resident(new_site)
                resident.set_path_finder(self._path_finder)
                print ('Generated resident')
                print (resident)

                new_site.add_resident(resident)

    def _get_immigration_by_zone_type(self, zone_density):

        immi_stats = {}
        # determine immigration for each zone type
        for tp, density in zone_density.items():

            prob = self._get_probability(tp, density)
            logging.debug(f' got prob %f density %f', prob, density)

            immi_stats[tp] = poisson.rvs(prob)

        return immi_stats

    def _generate_resident(self, new_site):

        # FIXME
        res_age = config.AGE_PDF_FARM.rand()
        res = Resident(res_age)

        site_type = new_site.get_zone_type()

        for skill, func in config.DEFAULT_SKILL_DISTS.items():
            res.set_skill(
                skill, 
                func.rand()[0] + config.SKILL_MODS.get(skill, 0)
            )

        for need, val in config.DEFAULT_NEED_RATES.items():
            res.set_need_rate(need, val)

        logger.debug('NEW SITE SHAPE')
        logger.debug(new_site.shape)
        res.location = (new_site.shape.x, new_site.shape.y)

        return res

    def _generate_site(self, ztype, shape, site_loc):

        zone = self.board.get_zones(zone_id = site_loc['zid'])

        trans_shape = affinity.translate(shape, xoff=site_loc.x, yoff=site_loc.y)
        print ('Create site at location')
        print (trans_shape)

        site = Farm(1, 1, trans_shape)

        site.set_zone(zone)

        add_success = zone.add_site_with_check(site)
        if not add_success:
            print ('Failed to add')
            raise RuntimeError('Failed to add site')

        return site

    def find_best_site(self, ztype):

        # get all occupied sites from all zones
        occupied_sites = []
        for z in self.board.get_zones():
            occupied_sites += z.sites
        
        scores = self.get_scores(ztype, occupied_sites)

        scores = scores[scores['comb_score'] > 0]

        print (scores)
        scores = scores[scores['comb_score'] == scores['comb_score'].max()]

        if scores.shape[0] == 0:
            return None

        rand_score = scores.iloc[random.randint(0, scores.shape[0]-1)]

        return rand_score

    def get_scores(self, ztype, occupied_sites):

        zones = self.board.get_zones(ztype)

        scores_df = []
        for z in zones:

            zid = z.id

            for x, y in z.iter_points():
                pt = Point(x, y)

                scores = {}
                scores['zid'] = zid
                scores['x'] = x
                scores['y'] = y

                scores['path_score'] = self._get_path_score(pt)

                scores['neighbor_score'] = self._get_neighbor_score(ztype, pt, occupied_sites)

                if not occupied_sites:
                    scores['overlap_score'] = 1
                else:
                    scores['overlap_score'] = min([int(not s.shape.contains(pt)) for s in occupied_sites])

                scores_df.append(scores)

        comb_df = pd.DataFrame.from_records(scores_df)
        # FIXME
        comb_df['comb_score'] = comb_df['neighbor_score'] * comb_df['path_score'] * comb_df['overlap_score']

        return comb_df

    def _get_neighbor_score(self, ztype, pt, sites):

        if not sites:
            return 1

        site_dists = []
        for site in sites:
            sid = site.id
            dists = []
            for x, y in site.iter_points():
                opt = Point(x, y)
                dists.append(pt.distance(opt))

            min_dist = min(dists)

            site_dists.append(min_dist)

        min_dist = min(site_dists)
        if ztype == zone_types.farm:
            return config.DISTANCE_SCORE_FARM.eval(min_dist)


    def _get_path_score(self, pt):

        # do we need scores for all paths?
        scores = []
        for p in self.board.paths:

            dist = p.get_shape().distance(pt)

            #score = dist
            score = config.PATH_SCORE_FARM.eval(dist)

            scores.append(score)

        if not scores:
            return 1
        else:
            return min(scores)


    def _get_probability(self, ztype, density):

        if ztype == zone_types.farm:
            prob = config.ATTRACTION_FARM.eval(density)
            return prob
        else:
            raise NotImplementedError('Must implement other zone types')
            return 0
            
    def get_movement_cost(self, point):
        pass
        # cannot know the movement cost
        # without knowing the mods
