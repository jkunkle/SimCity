from components.site import site
import communication

class output_slot:

    def __init__(self):

        self._destination = None
        self._is_posted = False

    def fill_slot(self, destination):

        self._destination = destination
        self._is_posted = False

    def set_posted(self):
        self._posted = True

    def is_posted(self):
        return self._is_posted

    def is_filled(self):
        return (self._destination is not None)


class business(site):

    def __init__(self,
                 zone_type,
                 total_jobs,
                 output_capacity,
                 needed_commercial_suppliers,
                 needed_industrial_suppliers,
                 shape):

        super().__init__(zone_type, shape)

        self._needed_c_suppliers = needed_commercial_suppliers
        self._needed_i_suppliers = needed_industrial_suppliers
        self._output_capacity = output_capacity
        self._total_jobs = total_jobs
        self._output_var = 0

        # FIXME -- Add details as needed
        self._output_slots = [output_slot() for _ in range(0, self._output_capacity)]
        self._jobs = [job() for _ in range(0, self._total_jobs)]

        self._curr_c_suppliers = 0
        self._curr_i_suppliers = 0

        # FIXME -- perhaps allow > 1 in future
        self._max_job_adverts = 1
        self._job_adverts = []
        self._max_slot_adverts = 1
        self._slot_adverts = []

        self._slot_applications = []
        self._job_applications = []

    def get_needed_i_suppliers(self):
        return self._needed_i_suppliers - self._curr_i_suppliers

    def get_needed_c_suppliers(self):
        return self._needed_c_suppliers - self._curr_c_suppliers

    def get_remaining_capacity(self):
        return self._output_capacity - self._curr_capacity

    def get_open_jobs(self):
        return self._total_jobs - self._curr_employees

    def add_slot_application(self, app):
        self._slot_applications.append(app)

    def generate_output(self):
        pass

        # how to generate output

    def generate_adverts(self, board):

        self.post_slot_advert(board)
        self.post_job_advert(board)


    def post_job_advert(self, board):

        if len(self._job_adverts) < self._max_job_adverts:

            job = self.get_postable_job()
            if job is None:
                return 

            adv = self.generate_advert(job)

            board.post_advert(adv)

    def get_postable_job(self):

        for j in self._jobs:
            if not j.is_filled() and not j.is_posted():
                return j

        return None


    def generate_advert(self, job):

        adv = communication.advert(self, job)

        return adv

    def post_slot_advert(self, board):

        if len(self._slot_adverts) < self._max_slot_adverts:

            slot = self.get_postable_slot()
            if slot is None:
                return 

            adv = self.generate_advert(slot)

            board.post_advert(adv)


    def get_postable_slot(self):

        for s in self._output_slots:
            if not s.is_filled() and not s.is_posted():
                return s

        return None

    def generate_applications(self, adverts):

        needed_i_suppliers = self.get_needed_i_suppliers()
        needed_c_suppliers = self.get_needed_c_suppliers()

        advert_scored = []

        if needed_i_suppliers > 0:
            for a in adverts:
                if a.get_source_type() == zone_types.industrial:
                    score = self._get_match_score(a)

                    advert_scored.append((score, a))
        if needed_c_suppliers > 0:
            for a in adverts:
                if a.get_source_type() == zone_types.commercial:
                    score = self._get_match_score(a)

                    advert_scored.append((score, a))

        advert_scored.sort(reverse=True)

        if not advert_scored:
            return

        self._send_slot_application(advert_scored[0][1])

    def _send_slot_application(self, advert):

        source = advert.get_source() 
        app = application(self)

        source.add_slot_application(app)


    def _get_match_score(self, other):

        #FIXME -- add more components here
        #FIXME -- may depned on zone type
        score = 1

        dist = utils.calc_distance(self, other)
        dist_score = config.distance_match(dist)

        score *= dist_score

        return score


    def resolve_applications(self):
        raise NotImplementedError


