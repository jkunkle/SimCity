import uuid
import definitions

class resident:

    def __init__(self, age):

        self._age = age
        self._is_employed = False
        self._uid = uuid.uuid4()
        self._needs = {}
        self._need_rates = {}
        self._skills = {}

        for n in definitions.needs:
            self._needs[n] = 1
            self._need_rates[n] = 0

        for s in definitions.skills:
            self._skills[s] = 0

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

    def increment(self, dt):
        # FIXME -- implement
        pass

    @property
    def c_slots(self):
        return self._c_slots

    @c_slots.setter
    def c_slots(self, other):
        self._c_slots = other

    def needs_job(self):
        return (self._is_employed == False) & (self._age >= 18)


    def display(self):

        stat = 'age = %f\n' %self._age

        for skill, val in self._skills.items():
            stat += '%s : %f\n' %(skill, val)

        print (stat)



