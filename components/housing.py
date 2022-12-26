from site import site
from zone import zone_types

class housing(site):

    def __init__(self, total_residences, shape):

        super().__init__(zone_types.residential, shape)

        self._total_residences = total_residences
        self._curr_residences = 0
        self._residents = []
        self._total_c_slots = c_slots
        self._curr_c_slots = 0

    def get_open_c_slots(self):
        return self._total_c_slots - self._curr_c_slots

    def get_needed_c_suppliers(self):

        needs = 0
        for r in self._residents:
            needs += r.get_open_c_slots()

        return needs

    def get_open_applications(self):

        n_open = 0
        for r in self._residents:
            if r.needs_job():
                n_open += 1

        return n_open

    def add_residents(self, n_residents):

        remain_residents = self._total_residences - len(self._residents)

        n_residents = min(remain_residents, n_residents)

        ages = [np.random.poisson(10) + 20 for x in range(0, n_residences)]
        edus = [1]*n_residences

        for age, edu in zip(ages, edus):
            c_slots = np.random.choice(config.HOUSING_COMMERCIAL_SLOTS)
            self._residents.append(resident(age, edu, c_slots))


