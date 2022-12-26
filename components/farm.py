from components.business import business
from components.zone import zone_types

class farm(business):

    def __init__(self, total_residences, output_capacity, shape):

        super().__init__(zone_types.farm, 0, output_capacity, 0, 0, shape)

        self._total_residences = total_residences
        self._curr_residences = 0
        self._residents = []
