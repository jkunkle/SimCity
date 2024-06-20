import uuid
import logging
import definitions
import config
from components import behavior

logger = logging.getLogger(__name__)

class Resident:

    def __init__(self, age):

        self._age = age
        self._location = None
        self._is_employed = False
        self._uid = uuid.uuid4()
        self._needs = {}
        self._need_rates = {}
        self._skills = {}
        self._health = {}
        self._movement_modifiers = {}
        self._behavior = behavior.Default()
        self._path_finder = None

        for n in definitions.needs:
            self._needs[n] = 1
            self._need_rates[n] = config.DEFAULT_NEED_RATES[n]

        for s in definitions.skills:
            self._skills[s] = 0

        for h in definitions.health_elements:
            self._health[h] = 1

        for t in definitions.terrain:
            self._movement_modifiers[t] = 1

    @property
    def c_slots(self):
        return self._c_slots

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, loc):
        self._location = loc

    @c_slots.setter
    def c_slots(self, other):
        self._c_slots = other

    def set_need(self, need, value):

        if need not in self._needs:
            raise ValueError(f'Need {need} is not known')
        self._needs[need] = value

    def set_need_rate(self, need, value):

        if need not in self._need_rates:
            raise ValueError(f'Need {need} is not known')
        self._need_rates[need] = value

    def set_skill(self, skill, value):

        if skill not in self._skills:
            raise ValueError(f'Skill {skill} is not known')
        self._skills[skill] = value

    def set_path_finder(self, pf):
        self._path_finder = pf

    def increment(self, dt):

        remain_dt = []
        for need, val in self._needs.items():
            rate = self._need_rates[need]

            self._needs[need] = val - dt*rate

            remain_dt.append((self._needs[need]/rate, need))

        # FIXME
        # do we need to get some needed resources from the behavior?
        #needed_resources += self._behavior.get_all_needs()

        self._update_connections()

        self._behavior.run(dt)
        # FIXME can reconsider
        # fill the most needed need
        # iteratively for each dt
        # FIXME does not work with float

        #needs_to_fill = []
        #for _ in range(0, dt):
        #    remain_dt.sort()
        #    remain_dt[0] = (remain_dt[0][0]+1, remain_dt[1])
        #    needs_to_fill.append(remain_dt[1])

    def _update_connections(self):

        movement_costs = {}
        for t, tcost in movement_costs:
            tmod = self._movement_modifiers[t]

            movement_costs[t] = tcost*tmod


        self._find_connection(movement_costs, definitions.needs.water)

    def _find_connection(self, movement_costs, need):

        #FIXME enable path finding
        return
        #self._path_finder.find_path(movement_costs, self.location, need)



    def needs_job(self):
        return (self._is_employed == False) & (self._age >= 18)


    def __repr__(self):

        stat = 'age = %f\n' %self._age

        for skill, val in self._skills.items():
            stat += '%s : %f\n' %(skill, val)

        return (stat)



