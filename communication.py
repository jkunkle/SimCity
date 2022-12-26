
class advert:

    def __init__(self, source, opening):

        self._source = source
        self._opening = opening

    def get_source(self):
        return self._source

    def is_job_advert(self):
        return isinstance(self._opening, job)
    def is_slot_advert(self):
        return isinstance(self._opening, output_slot)
    def get_source_type(self):
        return self._source.get_zone_type()



class application:

    def __init__(self, source, destination):

        self._source = source
        self._destination = destination
        self._match_score = None

        self.calculate_score()

    def calculate_score(self):



        self._match_score = score

