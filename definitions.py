
from enum import Enum

class zone_types(Enum):

    residential = 1
    commercial = 2
    industrial = 3
    farm = 4


class skills(Enum):

    hunting = 1
    gathering = 2
    forestry = 3
    plants = 4
    animal_husbandry = 5
    building = 6
    creativity = 7
    medical = 8 # need?
    learning = 9
    selling = 10

class needs(Enum):

    water = 1
    food = 2
    shelter = 3
    friend = 4
    partner = 5
    happiness = 6


class resource(Enum):

    water = 1
    forest = 2
    #FIXME -- add addtl resources

