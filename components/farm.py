from components.business import business
from components.zone import zone_types

import config

class Farm(business):

    def __init__(self, curr_residents, output_capacity, shape):

        # init the business part
        super().__init__(zone_types.farm, 0, output_capacity, 0, 0, shape)

        self._output_var = config.FARM_OUTPUT_VAR




        self._output_capacity = curr_residents + config.DEFAULT_EXCESS_OUTPUT_FARM
        self._curr_residents = curr_residents





