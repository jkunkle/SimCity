
class job:

    # FIXME -- pass additional job info
    def __init__(self):
        self._occupant = None
        self._is_posted = False

    def fill_job(self, occupant):
        self._occupant = occupant
        self._is_posted = False

    def set_posted(self):

        self._is_posted = True

    def is_posted(self):
        return self._is_posted

    def is_filled(self):
        return (self._occupant is not None)

