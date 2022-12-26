import uuid

class resident:

    def __init__(self, age, edu):

        self._age = age
        self._edu = edu
        self._is_employed = False
        self._uid = uuid.uuid4()

    @property
    def c_slots(self):
        return self._c_slots

    @c_slots.setter
    def c_slots(self, other):
        self._c_slots = other

    def needs_job(self):
        return (self._is_employed == False) & (self._age >= 18)


